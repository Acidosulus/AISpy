import datetime
from urllib.parse import urlsplit
from flask import render_template, render_template_string, flash, redirect, url_for, request, send_file

import common
from common import connection_fl, connection_url_ul, connection, db, session
import dialogs
import data_sourses
from click import echo, style
import pprint
from sqlalchemy import text
import models
from models import Users, UserObject, UserMessage
from flask_login import login_user, logout_user, current_user, login_required
printer = pprint.PrettyPrinter(indent=12, width=180)
prnt = printer.pprint
import pandas
import xlsxwriter
import os
import json
import ujson
import uuid
from common import app
from designerUL import Data_Construct
from celery.result import AsyncResult

from main import applicaton_mode
echo(style('applicaton_mode:', bg='blue', fg='bright_yellow')+style(applicaton_mode, bg='blue', fg='bright_green'))

from common import Celery_Tasks_Pull
task_pull = Celery_Tasks_Pull()


global celery_tasks
celery_tasks = {}


import threading
async def check_celery_tasks():
	if applicaton_mode != 'flask':
		return
	for id in list(task_pull.pull.keys()):
		if task_pull.pull[id].active:
			prnt(task_pull.pull[id].Information())
			if task_pull.pull[id].task.ready() and task_pull.pull[id].active:
				lnk = f'/download_report_from_file_store?file_name={task_pull.pull[id].task.get().replace("/","%2F")}'
				print("===============",lnk,"====================")
				with app.app_context():
					print('add message about task ending')
					# models.Add_Message_for_User(user_id=task_pull.pull[id].user_id, text='Конструктор отчетов', link=lnk, icon='excel', style='message_log_designer_ul_name')
					print('message added successfully')
				task_pull.pull[id].active = False
	threading.Timer(3, await check_celery_tasks).start()



data_sourses.init()

from statements import Reports, Points_WithOut_Displays, Points_with_Constant_Consuming, Pays_from_date_to_date, Points_Heads_And_Submissives
pull = Reports()
pull.add(Points_WithOut_Displays())
pull.add(Points_with_Constant_Consuming())
pull.add(Pays_from_date_to_date())
pull.add(Points_Heads_And_Submissives())



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
	return render_template("agreements.html",
							results=data,
							parents=data_sourses.get_agreements_hierarchy(int(object_id)),
							navigation_buttons = [common.Button_Home(), common.Agreements_Search(), common.Button_Back()])


@app.route('/')
@app.route('/index')
@login_required
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
			# it's a folder
			row['path'] = f'/page_with_items/{row["persistent_id"]}'
		else:
			# it's a item of list
			report_name = row['path'].replace('/Report/','')
			row['onclick'] = f"""openModal(`/Report_Get_Dialog_JSON/{report_name}`)"""
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

@app.route('/Report_Get_Dialog_JSON/<report_name>', methods=["GET", "POST"])
def Report_Get_Dialog_JSON(report_name):
	echo(style(text='Report:', fg='black', bg='white') + ' ' + style(text=report_name, fg='bright_white'))
	if report_name in pull.report_names_list():
		return pull.reports[report_name].report_dialog_JSON()
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
	echo(style(request.form.items(), fg='bright_red'))
	if report_name in pull.report_names_list():
		parameters = pull.reports[report_name].dialog.get_answers(request.form.items())
		echo(style(parameters, fg='bright_red'))
	echo(style('dialog answer: ', fg='yellow')+style(parameters, fg='bright_yellow'))
	if report_name in pull.report_names_list():
		return pull.reports[report_name].run_report(parameters, current_user.id)
	return redirect(url_for('index'))


@app.route('/addresses/<object_id>')
def addresses(object_id):
	print(object_id)
	header, results = data_sourses.Data_For_Addresses_List(object_id)
	return render_template("addresses.html", results=results, parents = data_sourses.get_addresses_hierarchy(int(object_id)), navigation_buttons = [common.Button_Home(), common.Button_Back()])


def generate_select_options_html( header_data:tuple, current_row_id=0):
	header = header_data[0]
	data =header_data[1]
	result = ''
	for row in data:
		st = ''
		for key, value in row.items():
			if key != 'row_id':
				st += ' '+value
		result += f"""<option value="{row[header[0]]}" {( 'selected' if current_row_id == row[header[0]] else '')}>{st}</option>\n"""
	return result


@app.route('/agreement_form/<row_id>')
def agreement_form(row_id:int):
	header, fdata = data_sourses.Agreement_Data(int(row_id))
	header, agreement_types_data = data_sourses.Agreement_Types_Data()
	header, agreement_parameters = data_sourses.Agreement_Parameters_Data(int(row_id))
	header, agreement_payments_scedule = data_sourses.Agreement_Payments_Schedule(int(row_id))
	header, agreement_points_list = data_sourses.Points_Data(int(row_id))
	header, agreement_documents = data_sourses.Agreement_Documents_List(int(row_id))
	prnt(agreement_documents)
	#header, calc_data = data_sourses.Calc_Data(int(row_id))
	return render_template("/forms/agreement_form/agreement_form.html",
							fdata = fdata[0],
							agreement_types_data = agreement_types_data,
							agreement_parameters = agreement_parameters,
							agreement_payments_scedule = agreement_payments_scedule,
							html_for_select_agreement_types = generate_select_options_html( data_sourses.Ref_Agreement_Types(), fdata[0]['agr_type'] ),
							agreement_points_list = agreement_points_list,
							agreement_documents = agreement_documents
							)


@app.route('/agreement_form_part_calc_table/<row_id>/<period>')
def agreement_form_part_calc_table(row_id:int,period:str):
	header, calc_data = data_sourses.Calc_Data(int(row_id),period)
	return render_template("/forms/agreement_form/__form_calc_table.html",
							calc_data = calc_data
							)


@app.route('/reports_builder_ul')
@login_required
def reports_builder_ul():
	return render_template("/forms/reports_builder/reports_builder_ul/reports_builder_ul.html",
							navigation_buttons = [common.Button_Home(), common.Button_Back()]
							)

@app.route('/organization_form/<row_id>')
def organization_form(row_id:int):
	header, fdata = data_sourses.Organization_Data(int(row_id))
	return render_template("/forms/organization_form/organization_form.html",
							row_id = row_id,
							fdata = fdata[0],
							html_for_select_organization_vid = generate_select_options_html( data_sourses.Ref_Organizaion_Vid(), fdata[0]['org_vid_id']),
							html_for_select_organization_type = generate_select_options_html( data_sourses.Ref_Organizaion_Type(), fdata[0]['org_type_id']),
							html_for_select_organization_NDS = generate_select_options_html( data_sourses.Ref_Organizaion_NDS(), fdata[0]['nds_type']),
							html_for_select_organization_Debtor_Category = generate_select_options_html( data_sourses.Ref_Organizaion_Debtor_Category(), fdata[0]['debtor_category']),
							navigation_buttons = [common.Button_Home(), common.Button_Back(), ])



@app.route('/agreement_search_form')
def agreement_search_form():
	return render_template("/forms/search_form/search_form.html",
							)

@app.route('/get_agremments_search_result', methods=["POST"])
def get_agremments_search_result():
	header, results = data_sourses.Agreements_Search_Data(request.get_json()['search_substring'])
	return render_template("/forms/search_form/_agreements.html",	
							results = results
							)


@app.route('/test/')
def test():
	#header, fdata = data_sourses.Agreement_Data(int(row_id))
	return render_template("/forms/organization_form/organization_form.html",
							navigation_buttons = [common.Button_Home(), common.Button_Back()])


@app.route('/get_organization_data/<row_id>', methods=["GET", "POST"])
def get_organization_data(row_id:int):
	header, data = data_sourses.Organization_Data(int(row_id))
	return ujson.dumps(data[0], sort_keys=False, ensure_ascii=False)






















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


@app.route("/test_dialog", methods=['GET', 'POST'])
def test_dialog():
	return str(dialogs.dialogtest)


@app.route("/designer_ul_clear_data_endpoint", methods=['GET', 'POST'])
def designer_ul_clear_data_endpoint():
	designer_ul_clear_data(current_user.id)
	return ''

def designer_ul_clear_data(user_id:int):
	connection.execute(db.update(models.UserObject).where(models.UserObject.user_id==user_id, models.UserObject.name=='data_designer_ul').values(data='{}'))
	connection.commit()
	return ''

# get record designer_ul for user_id
def designer_ul_get_data_id(user_id):
	return connection.execute(
			db.select(models.UserObject).
			where(	models.UserObject.user_id==user_id,
		 			models.UserObject.name=='data_designer_ul')).first()
	

@app.route("/designer_ul_clear_data_parameters", methods=['GET', 'POST'])
def designer_ul_clear_data_parameters():
	connection.execute(db.update(models.UserObject).where(models.UserObject.user_id==current_user.id, models.UserObject.name=='data_designer_ul').values(parameters='[]'))
	connection.commit()
	return ''


@app.route("/designer_ul_add_all_agreements", methods=['GET', 'POST'])
def designer_ul_add_all_agreements():
	designer_ul_clear_data(current_user.id)
	
	head, data = data_sourses.All_Agreement_Numbers()

	user_object = designer_ul_get_data_id(current_user.id)
	if user_object == None:
		user_object = UserObject(	user_id = current_user.id,
									name = 'data_designer_ul',
									data = json.dumps(data),
									dt= datetime.date.today()	)
	else:
		user_object = db.session.query(models.UserObject).filter(models.UserObject.user_id==current_user.id, models.UserObject.name=='data_designer_ul').first()
		user_object.data  = json.dumps(data)

	db.session.add(user_object)
	db.session.commit()
	return 'ok'


@app.route("/designer_ul_add_opened_agreements", methods=['GET', 'POST'])
def designer_ul_add_opened_agreements():
	designer_ul_clear_data(current_user.id)

	head, data = data_sourses.Opened_Agreement_Numbers()

	user_object = designer_ul_get_data_id(current_user.id)
	if user_object == None:
		user_object = UserObject(	user_id = current_user.id,
									name = 'data_designer_ul',
									data = json.dumps(data),
									dt= datetime.date.today()	)
	else:
		user_object = db.session.query(models.UserObject).filter(models.UserObject.user_id==current_user.id, models.UserObject.name=='data_designer_ul').first()
		user_object.data  = json.dumps(data)
		
	db.session.add(user_object)
	db.session.commit()
	return 'ok'


@app.route("/designer_ul_add_all_points", methods=['GET', 'POST'])
def designer_ul_add_all_points():
	designer_ul_clear_data(current_user.id)

	head, data = data_sourses.All_Point_Numbers()

	user_object = designer_ul_get_data_id(current_user.id)
	if user_object == None:
		user_object = UserObject(	user_id = current_user.id,
									name = 'data_designer_ul',
									data = json.dumps(data),
									dt= datetime.date.today()	)
	else:
		user_object = db.session.query(models.UserObject).filter(models.UserObject.user_id==current_user.id, models.UserObject.name=='data_designer_ul').first()
		user_object.data  = json.dumps(data)

	db.session.add(user_object)
	db.session.commit()
	return 'ok'

@app.route("/designer_ul_add_all_points_of_opened_agreements", methods=['GET', 'POST'])
def designer_ul_add_all_points_of_opened_agreements():
	designer_ul_clear_data(current_user.id)

	head, data = data_sourses.Point_Numbers_of_Opened_Agreements()

	user_object = designer_ul_get_data_id(current_user.id)
	if user_object == None:
		user_object = UserObject(	user_id = current_user.id,
									name = 'data_designer_ul',
									data = json.dumps(data),
									dt= datetime.date.today()	)
	else:
		user_object = db.session.query(models.UserObject).filter(models.UserObject.user_id==current_user.id, models.UserObject.name=='data_designer_ul').first()
		user_object.data  = json.dumps(data)

	db.session.add(user_object)
	db.session.commit()
	return 'ok'

@app.route("/designer_ul_get_source", methods=['GET', 'POST'])
def designer_ul_get_source():
	data = connection.execute(db.select(models.UserObject).where(models.UserObject.user_id==current_user.id, models.UserObject.name=='data_designer_ul')).first()
	if data!=None:
		return json.loads(data.data)
	return ''

@app.route("/designer_ul_get_source_parameters", methods=['GET', 'POST'])
def designer_ul_get_source_parameters():
	data = connection.execute(db.select(models.UserObject).where(models.UserObject.user_id==current_user.id, models.UserObject.name=='data_designer_ul')).first()
	if data!=None:
		return json.loads(data.parameters)
	return ''



@app.route("/insert_data_agreements_from_clipboard", methods=['GET', 'POST'])
def insert_data_agreements_from_clipboard():
	designer_ul_clear_data(current_user.id)
	agreements = f"""{request.get_data().decode('utf-8').strip()}""".split('\n')
	dict_list = []
	for agreement in agreements:
		dict_list.append({'agreement':agreement, 'point':'		  '})
	print('inserted data:', dict_list)

	user_object = designer_ul_get_data_id(current_user.id)
	if user_object == None:
		user_object = UserObject(	user_id = current_user.id,
									name = 'data_designer_ul',
									data = json.dumps(dict_list),
									dt= datetime.date.today()	)
	else:
		user_object = db.session.query(models.UserObject).filter(models.UserObject.user_id==current_user.id, models.UserObject.name=='data_designer_ul').first()
		user_object.data  = json.dumps(dict_list)

	
	
	
	
	
	db.session.add(user_object)
	db.session.commit()
	return ''


@app.route("/insert_data_points_from_clipboard", methods=['GET', 'POST'])
def insert_data_points_from_clipboard():
	designer_ul_clear_data(current_user.id)
	points = f"""{request.get_data().decode('utf-8').strip()}""".split('\n')

	pointsagrs={}
	head, data = data_sourses.All_Point_Numbers()
	for row in data:
		if len(row['point'].strip())==10 and len(row['agreement'].strip())==10:
			pointsagrs[ row['point'].strip() ] = row['agreement'].strip()

	dict_list = []
	for point in points:
		dict_list.append({'agreement':(pointsagrs[point.strip()] if point.strip() in pointsagrs else '		  '), 'point':point.strip()})

	print('inserted data:', dict_list)

	
	user_object = designer_ul_get_data_id(current_user.id)
	if user_object == None:
		user_object = UserObject(	user_id = current_user.id,
									name = 'data_designer_ul',
									data = json.dumps(dict_list),
									parameters='[]',
									dt= datetime.date.today()	)
	else:
		user_object = db.session.query(models.UserObject).filter(models.UserObject.user_id==current_user.id, models.UserObject.name=='data_designer_ul').first()
		user_object.data  = json.dumps(dict_list)
	
	
	db.session.add(user_object)
	db.session.commit()
	return ''
"""
@app.route("/designer_ul_add_data", methods=['POST','GET'])
def designer_ul_add_data():
	print(f"==============>>{json.loads(request.get_data())}")
	response = json.loads(request.get_data())
	echo(style(text=request.get_data(), fg='bright_yellow'))
	echo(style(text=type(request.get_data()), fg='bright_green'))
	echo(style(text=response, fg='bright_cyan'))
	echo(style(text=type(response), fg='bright_blue'))
	if 'type' in response:
			user_object = designer_ul_get_data_id(current_user.id)
			if user_object == None:
				user_object = UserObject(	user_id = current_user.id,
											name = 'data_designer_ul',
											data = 	'',
											parameters=json.dumps([response]),
											dt= datetime.date.today()	)
				db.session.add(user_object)
			else:
				user_object = db.session.query(models.UserObject).filter(models.UserObject.user_id==current_user.id, models.UserObject.name=='data_designer_ul').first()
				
				parameterst = json.loads((user_object.parameters if type(user_object.parameters)==str else '[]'))
				parameterst.append(response)
				user_object.parameters = json.dumps(parameterst, ensure_ascii=False)
				db.session.add(user_object)
	db.session.commit()
	return ''
"""

@app.route("/designer_ul_add_data", methods=['POST','GET'])
def designer_ul_add_data():
	print('>>>>>>>>>>>>>>>>>>>>>>>')
	print(f"{json.loads(request.get_data())}")
	response = json.loads(request.get_data())
	if 'type' in response:
			user_object = designer_ul_get_data_id(current_user.id)
			if user_object == None:
				user_object = UserObject(	user_id = current_user.id,
											name = 'data_designer_ul',
											data = 	'',
											parameters=f'[{response}]',
											dt= datetime.date.today()	)
				db.session.add(user_object)
			else:
				user_object = db.session.query(models.UserObject).filter(models.UserObject.user_id==current_user.id, models.UserObject.name=='data_designer_ul').first()
				parameterst = json.loads(user_object.parameters)
				parameterst.append(response)
				user_object.parameters = json.dumps(parameterst, ensure_ascii=False)
				db.session.add(user_object)
	db.session.commit()
	return ''


@app.route("/designer_ul_get_excel_result", methods=['POST','GET'])
def designer_ul_get_excel_result():
	echo(style(text='designer_ul_get_excel_result', fg='bright_red'))
	user_object = designer_ul_get_data_id(current_user.id)
	prnt(user_object)
	if user_object == None:
		echo(text='break',bg='red')
		return ''

	task = Data_Construct.apply_async([current_user.id, user_object.data, user_object.parameters])
	ctask = task_pull.add_task(task, current_user.id, 'file_download')
	echo(style(text=f'{datetime.datetime.now()} task added: {ctask.Information()}', fg='bright_red'))

	return ctask.id


@app.route('/Check_Celery_Task_Status', methods=['POST'])
def Check_Celery_Task_Status():
	arguments = f"""{request.get_data().decode('utf-8').strip()}""".split('\n')
	uid = json.loads(arguments[0])['uid']+'_'+str(current_user.id)
	print('celery_tasks: ', celery_tasks)
	print(uid)
	
	task = task_pull.pull[json.loads(arguments[0])['uid']]
	if task.user_id == current_user.id:
		if task.task.ready():
			if task.task.successful():
				return task.task.get()
	return ''


@app.route('/download_report_from_file_store', methods=['GET'])
def download_report_from_file_store():
	file_name = request.args.get('file_name').replace('"','')
	prnt({'file_name':file_name})
	return send_file(file_name)


@app.route('/message_log',methods=['POST'])
def get_message_log():
	query_result = session.	query(models.UserMessage).\
							filter(	models.UserMessage.user_id==current_user.id).\
							order_by(models.UserMessage.dt).all()
	messages = common.RowsToDictList(query_result)
	return messages


@app.route('/show_text/<object_id>',methods=['GET'])
def show_text(object_id:int):
	query = session.	query(	models.UserObject).\
						filter(	models.UserObject.user_id==current_user.id,
		 						models.UserObject.id==object_id ).first()
	result = common.RowToDict(query)
	return render_template("show_text.html", text = result['data'])


@app.route('/db_services',methods=['GET'])
def db_services():
	return render_template("db_services.html",)


@app.route('/ul_regain_statistic',methods=['GET'])
def ul_regain_statistic():
	data_sourses.Update_Statistic_UL_DB(current_user.id)
	return ''