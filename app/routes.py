from datetime import datetime, timezone
from urllib.parse import urlsplit
from flask import render_template, render_template_string, flash, redirect, url_for, request, send_file
from app import app, db, models,connection_fl, dialogs, common, data_sourses, pull, connection, data_sourses
from click import echo, style
import pprint
from sqlalchemy import text
from app.models import Users
from flask_login import login_user, logout_user, current_user
printer = pprint.PrettyPrinter(indent=12, width=180)
prnt = printer.pprint
import pandas
import xlsxwriter
import os
import json


@app.route('/agreements/<object_id>')
def agreements(object_id:int):
	print(object_id)
	header, data = data_sourses.Data_For_Agreements_List(object_id)
	print('===============agreements=================')
	for row in data:
		#print(type(row['descendants_count']))
		#if isinstance(type(row['descendants_count']), int):
		#	print(type(row['descendants_count']))
		#prnt(row)
		row['descendants_count'] =  int(row['descendants_count'])
	return render_template("agreements.html", results=data, parents=data_sourses.get_agreements_hierarchy(int(object_id)), navigation_buttons = [common.Button_Home(), common.Button_Back()])


@app.route('/')
@app.route('/index')
def index():
	##### working db insert code ######
	#u = models.User(nickname='john', email='john@email.com', role=models.ROLE_ADMIN)
	#db.session.add(u)
	#db.session.commit()
	##############################
#	print('from route: ',connection_fl)
	user = {'nickname':'UserName'}
	title = 'AISpy' if current_user.is_authenticated else 'Вход в систему не выполнен'
	print('=============---==============')
	#prnt(data_sourses.Points_WithOut_Displays(2023,1))
	return render_template("main_index.html", title = title, user = user)


@app.route('/parameters_dialog/')
def parameters_dialog():
	return render_template("parameters_dialog.html", parametesJSON = str(dialogs.testdialog))


@app.route('/Report_From_History/<report_name>/<user_data_id>')
def report_from_history(report_name:str, user_data_id:int):
	echo(style(text='Report:', fg='black', bg='white') + ' ' + style(text='report_from_history', fg='bright_white'))
	echo(style(text='report_name:', fg='black', bg='white') + ' ' + style(text=f'{report_name}', fg='bright_white'))
	echo(style(text='user_data_id:', fg='black', bg='white') + ' ' + style(text=f'{user_data_id}', fg='bright_white'))
	if report_name in pull.report_names_list():
		return pull.reports[report_name].report_from_history(current_user.id, user_data_id)
	return redirect(url_for('index'))


@app.route('/page_with_items/<parent_id>')
def page_with_items(parent_id):
	echo(style(text=f'page_with_items/{parent_id}', bg='blue', fg='bright_green'))
	rows = common.RowsToDictList(db.session.query(models.PageItemsList).filter(models.PageItemsList.parent==parent_id).all())
	print('rows:',rows)
	print(f'Reports',pull.reports)
	for row in rows:
		# item comment input into text field
		if len(row['note'])>0:
			if row['note'] != 'None':
				row['text'] = row['note']

		if len(row['path'])==0:
			row['path'] = f'/page_with_items/{row["persistent_id"]}'
		else:
			report_name = row['path'].replace('/Report/','')
			if len(report_name)>0:
				if report_name in pull.report_names_list():
					history_records_count = pull.reports[report_name].ready_reports_count(current_user.id)
					print(f'report_name found:{report_name}')
					print('ready_reports_count found:', history_records_count)
					if history_records_count>0:
						row['history_link'] = f'/report_history/{report_name}'
						row['history_records_count'] = history_records_count
	reportsList = rows
	return render_template("reports_index.html",
							reports=reportsList,
							list_title = 'Отчёты',
							parents = data_sourses.get_reports_hierarchy(int(parent_id)),
							navigation_buttons = [common.Button_Home(), common.Button_Back()])


@app.route('/delete_report/<report_id>')
def delete_report(report_id):
	echo(style(text='delete_report:', fg='black', bg='white') + ' ' + style(text=report_id, fg='bright_white'))
	echo(style(text='current_user.id:', fg='bright_white', bg='green'))
	report_data = connection.execute(db.select(models.UserObject.name).where(models.UserObject.id==report_id)).fetchall()
	print('Report name:', common.RowsToDictList(report_data)[0]['name'])
	connection.execute(db.delete(models.UserObject).where(models.UserObject.id==report_id))
	return redirect(url_for('report_history', report_name=common.RowsToDictList(report_data)[0]['name']))


@app.route('/report_history/<report_name>')
def report_history(report_name):
	echo(style(text='report_history:', fg='black', bg='white') + ' ' + style(text=report_name, fg='bright_white'))
	echo(style(text='current_user.id:', fg='bright_white', bg='green'))
	if report_name in pull.report_names_list():
		return pull.reports[report_name].history(current_user.id)
	return redirect(url_for('index'))

@app.route('/Report/<report_name>')
def Report(report_name):
	echo(style(text='Report:', fg='black', bg='white') + ' ' + style(text=report_name, fg='bright_white'))
	if report_name in pull.report_names_list():
		return pull.reports[report_name].report()
	return redirect(url_for('index'))


@app.route('/download_excel/<user_object_id>')
def download_excel(user_object_id):
	row = common.RowToDict( db.session.query(models.UserObject).filter(models.UserObject.id==user_object_id).first() )
	report_name = row['name']
	if report_name in pull.report_names_list():
		return pull.reports[report_name].download_excel(row['id'])
	return redirect(url_for('index'))


@app.route('/RunReport/<report_name>', methods=['POST'])
def RunReport(report_name):
	echo(style(text='Report:', fg='black', bg='white') + ' ' + style(text=report_name, fg='bright_white'))
	if report_name in pull.report_names_list():
		parameters = pull.reports[report_name].dialog.get_answers(request.form.items())
	echo(style('dialog answer: ', fg='yellow')+style(parameters, fg='bright_yellow'))
	if report_name in pull.report_names_list():
		return pull.reports[report_name].run_report(parameters, current_user.id)
	return redirect(url_for('index'))


@app.route('/addresses/<object_id>')
def addresses(object_id):
	print(object_id)
	header, results = data_sourses.Data_For_Addresses_List(object_id)
	return render_template("addresses.html", results=results, parents = data_sourses.get_addresses_hierarchy(int(object_id)), navigation_buttons = [common.Button_Home(), common.Button_Back()])



@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = Users(username=request.form.get("username"),
                     password=request.form.get("password"))
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("register.html")
 
 
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = Users.query.filter_by(
            username=request.form.get("username")).first()
        if user.password == request.form.get("password"):
            login_user(user)
            return redirect(url_for("index"))
    return render_template("login.html", title = "Вход в систему")
 
 
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))











