from datetime import datetime, timezone
from urllib.parse import urlsplit
from flask import render_template, render_template_string, flash, redirect, url_for, request, send_file
from app import app, db, models,connection_fl, dialogs, common, data_sourses, pull, connection
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

# get list of addresses of people with given parent_id
def Get_Addresses_List(parent_id:int) -> list:
	rez = connection_fl.execute(text(f"select stack.[AddrLs](row_id,0) as address, row_id, Номер as number  from stack.[Лицевые счета] where [Счета]={parent_id};")).fetchall()
	result = []
	for element in rez:
		result.append({'address':element[0], 'row_id':element[1], 'number':str(element[2])})
	return result


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


@app.route('/page_with_items/<parent_id>')
def page_with_items(parent_id):
	parent_name = connection.execute(db.select(models.PageItemsList.name).where(models.PageItemsList.persistent_id==parent_id) ).fetchone()
	try:
		parent_name = parent_name[0]
	except:
		parent_name = ''

	rows = common.RowsToDictList(db.session.query(models.PageItemsList).filter(models.PageItemsList.parent==parent_id).all())
	prnt(rows)
	print()
	for row in rows:
		if len(row['path'])==0:
			row['path'] = f'/page_with_items/{row["persistent_id"]}'
	prnt(rows)
	reportsList = rows
	return render_template("reports_index.html", reports=reportsList, list_title = 'Отчёты', list_sub_title = parent_name)


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
	parameters = dialogs.testdialog.get_answers(request.form.items())
	echo(style('dialog answer: ', fg='yellow')+style(parameters, fg='bright_yellow'))
	if report_name in pull.report_names_list():
		return pull.reports[report_name].run_report(parameters, current_user.id)
	return redirect(url_for('index'))


@app.route('/addresses/<object_id>')
def addresses(object_id):
	print(object_id)
	results = Get_Addresses_List(object_id)
	return render_template("addresses.html", results=results)


@app.route('/drop_all/')
def drop_all():
	db.drop_all()
	return redirect(url_for('index'))


@app.route('/create_all/')
def create_all():
	db.create_all()
	return redirect(url_for('index'))


@app.route('/import_data/')
def import_data():
	
	db.session.add(models.PageItemsList(	name = 'ТУ не имеющие показаний в расчётном периоде',
									 		path='/Report/ReportPointsWithoutDisplays',
											icon='/static/images/ico_excel.bmp',
											roles='0',
											persistent_id=1900,
											parent=-110))

	db.session.add(models.PageItemsList(   name='Рассчитанность ТУ МКЖД',
									path='/Report/Report_Calc_Status_MKJD_Points',
									icon='/static/images/ico_excel.bmp',
									roles='0',
									persistent_id=1901,
									parent= -110)
					)

	db.session.add(models.PageItemsList(   name='Сервисные отчёты по статусу расчёта текущего периода',
									path='',
									icon='/static/images/report.png',
									roles='0',
									persistent_id= -110,
									parent=-100)
					)

	db.session.add(models.PageItemsList(   name='Отчёты ЮЛ',
									path='',
									icon='/static/images/report.png',
									roles='0',
									persistent_id= -100,
									parent=-10)
					)
	db.session.add(models.PageItemsList(   name='Отчёты ФЛ',
									path='',
									icon='/static/images/report.png',
									roles='0',
									persistent_id= -200,
									parent=-10)
					)
	



	db.session.commit()
	return redirect(url_for('index'))







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











