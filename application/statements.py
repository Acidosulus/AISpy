import datetime
from flask import render_template, flash, redirect, url_for, request, send_file
from collections.abc import Iterable
from common import db, connection_fl, db,  connection
import models
import dialogs
import data_sourses
import common
from celery.result import AsyncResult
from click import echo, style
import json
import pandas
import xlsxwriter
import os
from sqlalchemy import func
from common import celery
from common import app

import pprint
printer = pprint.PrettyPrinter(indent=12, width=180)
prnt = printer.pprint

TMP_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'tmp')




def last_day_of_month(any_day):
    # The day 28 exists in every month. 4 days later, it's always next month
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)
    # subtracting the number of the current day brings us back one month
    return next_month - datetime.timedelta(days=next_month.day)



# @app.teardown_appcontext
def get_human_readable_report_name(report_name):
	report_humanread_name = connection.execute(db.select(models.PageItemsList.name).where(models.PageItemsList.path==f'/Report/{report_name}')).fetchone()
	try:
		report_humanread_name = report_humanread_name[0]
	except:
		report_humanread_name = ''
	return report_humanread_name

# @app.teardown_appcontext
def get_report_note(report_name):
	report_note = connection.execute(db.select(models.PageItemsList.note).where(models.PageItemsList.path==f'/Report/{report_name}')).fetchone()
	try:
		report_note = report_note[0]
	except:
		report_note = ''
	return report_note


# superclass for any report
class Report:
	def __init__(self):
		self.report_name = ''
		self.get_data_source_procedure_name = ''
		self.report_humanread_name = get_human_readable_report_name(self.report_name)
		self.note = get_report_note(self.report_name)

	def ready_reports_count(self, user_id:int) -> int:
		ready_reports_count = connection.execute(db.select(func.count(models.UserObject.id)).where(	models.UserObject.user_id == user_id,
														   								models.UserObject.name == self.report_name)).scalar()
		return ready_reports_count
	
	# return answer for start report with parameters dialog	
	def report(self):
		return render_template("parameters_dialog.html", parametesJSON = str(self.dialog), report_name=self.report_name, navigation_buttons = [common.Button_Home(), common.Button_Back()])
	
	# return answer for start report from last formed data, recieved UserData.id
	def report_from_history(self, user_id, user_data_id:int):
		echo(style(text='report_from_history into class', bg='blue', fg='bright_yellow'))
		row = common.RowsToDictList(connection.execute(db.select(	models.UserObject)
															.where(	models.UserObject.user_id == user_id,
					  												models.UserObject.name == self.report_name,
																	models.UserObject.id == user_data_id))
															.fetchall())[0]		
		parameters = json.loads(row['parameters'])
		data = json.loads(row['data'])
		df = pandas.DataFrame(data)
		return render_template("report.html", 
						 	data=df.to_html(classes='table table-success table-striped table-hover table-bordered border-primary align-middle' ), 
							report_title=f"{self.report_humanread_name}  {self.get_parameters_human_readable_string(parameters)}",
							data_object_id=user_data_id,
							report_name = self.report_name,
							navigation_buttons =	[	common.Button_Home(),
														common.Button_Back(),
														common.Button_List(href=f"/report_history/{self.report_name}"),
														common.Button_Excel(href=f"/download_excel/{user_data_id}")])

	def report_dialog_JSON(self):
		return str(self)
	
	#return history information humanreadable data from report parameters
	def get_report_history_information(self, parameters:dict) -> list :
		return []

	# return answer for report_history
	def history(self, user_id):
		rows = common.RowsToDictList(connection.execute(db.select(	models.UserObject.id,
																	models.UserObject.dt,
																	models.UserObject.parameters)
															.where(	models.UserObject.user_id == user_id,
					  												models.UserObject.name == self.report_name))
															.fetchall())
		reportsList = []
		for row in rows:
			foo = {}
			foo['path'] = f'/download_excel/{row["id"]}'
			foo['icon'] = f'/static/images/excel.png'
			foo['name'] = f'{self.report_humanread_name}'
			dparameters = json.loads(row["parameters"])
			dparameters['id'] = row["id"]
			dparameters['dt'] = row["dt"]
			foo['text']   = self.get_report_history_information(dparameters)[0] #f'Идентификатор результата: {row["id"]}'
			foo['text_1'] = self.get_report_history_information(dparameters)[1] #f'Год: {json.loads(row["parameters"])["year"]}'
			foo['text_2'] = self.get_report_history_information(dparameters)[2] #f'Месяц: {json.loads(row["parameters"])["month"]}'
			foo['text_3'] = self.get_report_history_information(dparameters)[3] #f'Время формирования: {row["dt"]:%Y-%m-%d %H:%M}'
			foo['delete_link'] = f"""/delete_report/{row["id"]}"""
			foo['view_link'] = f"""/Report_From_History/{self.report_name}/{row["id"]}"""
			reportsList.append(foo)
		return render_template("reports_index.html",
						 		reports=reportsList,
								list_title = self.report_humanread_name,
								list_sub_title = 'история формирования отчёта',
								navigation_buttons = [common.Button_Home(), common.Button_Back()])
	

	# return answer excel report file download
	def download_excel(self, user_object_id):
		row = common.RowToDict( db.session.query(models.UserObject).filter(models.UserObject.id==user_object_id).first() )
		report_humanread_name = get_human_readable_report_name(row["name"]) 
		data = json.loads(row['data'])
		parameters = json.loads(row['parameters'])
		df = pandas.DataFrame(data)
		file_name = os.path.join(TMP_FOLDER, f'report_id_{user_object_id}.xlsx')
		writer = pandas.ExcelWriter(file_name, engine='xlsxwriter')
		df.to_excel(writer, index=False, float_format="%.2f", startrow=4, freeze_panes=(5,0), sheet_name='report')
		writer.sheets['report'].autofilter('A5:WW5')
		writer.sheets['report'].write(0,0,report_humanread_name + self.get_parameters_human_readable_string(parameters))
		for column in df:
			writer.sheets['report'].set_column(
												df.columns.get_loc(column),
												df.columns.get_loc(column),
												max(df[column].astype(str).map(len).max(), len(column))
											)
		writer.close()
		return send_file(file_name)
	# return data source for report, must be realeased for every reportse separately
	def get_data_source(self, parameters, current_user_id:int):
		pass

	# return human readable parameters string for report title, must be realeased for every reportse separately
	def get_parameters_human_readable_string(self, parameters):
		return f"""{parameters}"""

	def __str__(self):
		return 'Report Superclass'


	# return answer for view report into browser
	def run_report(self, parameters, current_user_id):
		Create_Report.apply_async(  [	parameters,
										current_user_id,
										self.__class__.__name__,
										self.report_name,
										self.report_humanread_name,
										self.get_parameters_human_readable_string(parameters)
									]
									)
		return redirect(url_for('index'))
		#create new data set for new report
		header, data = self.get_data_source(parameters, current_user_id)
		data_object = models.UserObject(user_id=current_user_id,
										dt=datetime.date.today(),
										name=self.report_name,
										parameters=json.dumps(parameters, ensure_ascii=False),
										data=json.dumps(data, ensure_ascii=False))
		db.session.add(data_object)
		db.session.flush()
		data_object_id = data_object.id
		db.session.commit()
		df = pandas.DataFrame(data)
		models.Add_Message_for_User(	user_id=current_user_id,
							  			text=f"{self.report_humanread_name} {self.get_parameters_human_readable_string(parameters)}",
										link=f"/download_excel/{data_object_id}",
										icon='excel',
										style='message_log_report_name_excel')
		models.Add_Message_for_User(	user_id=current_user_id,
							  			text=f"{self.report_humanread_name} {self.get_parameters_human_readable_string(parameters)}",
										link=f"/Report_From_History/{self.report_name}/{data_object_id}",
										icon='table',
										style='message_log_report_name_table')

		return render_template("report.html", 
						 	data=df.to_html(classes='table table-success table-striped table-hover table-bordered border-primary align-middle' ), 
							report_title=f"{self.report_humanread_name} {self.get_parameters_human_readable_string(parameters)}",
							data_object_id=data_object_id,
							report_name = self.report_name,
							navigation_buttons = [	common.Button_Home(),
							 						common.Button_Back(),
													common.Button_List(href=f"/report_history/{self.report_name}"),
													common.Button_Excel(href=f"/download_excel/{data_object_id}")])
	

@celery.task()
def Create_Report(	parameters,
				  	current_user_id,
					report_class_object_name,
					report_name,
					report_humanread_name,
					parameters_human_readable_string):
		with app.app_context():
			obj = eval(f'{report_class_object_name}()')
			header, data = obj.get_data_source(parameters, current_user_id)
			data_object = models.UserObject(user_id=current_user_id,
											dt=datetime.date.today(),
											name=report_name,
											parameters=json.dumps(parameters, ensure_ascii=False),
											data=json.dumps(data, ensure_ascii=False))
			db.session.add(data_object)
			db.session.flush()
			data_object_id = data_object.id
			db.session.commit()
			df = pandas.DataFrame(data)
			models.Add_Message_for_User(	user_id=current_user_id,
											text=f"{report_humanread_name} {parameters_human_readable_string}",
											link=f"/download_excel/{data_object_id}",
											icon='excel',
											style='message_log_report_name_excel')
			models.Add_Message_for_User(	user_id=current_user_id,
											text=f"{report_humanread_name} {parameters_human_readable_string}",
											link=f"/Report_From_History/{report_name}/{data_object_id}",
											icon='table',
											style='message_log_report_name_table')


class Points_WithOut_Displays(Report):
	def __init__(self):
		self.report_name = 'ReportPointsWithoutDisplays'
		self.report_humanread_name = get_human_readable_report_name(self.report_name)
		self.dialog = dialogs.DialogParameters(title = get_human_readable_report_name(self.report_name), backlink=f'/RunReport/{self.report_name}')
		self.dialog.add_months('Месяц','month')
		self.dialog.add_years('Год','year')
		self.get_data_source_procedure_name = 'data_sourses.Points_WithOut_Displays'
		#self.dialog.add_checkbox('Открыть последний отчет от этих параметров','last',0)
	
	def get_parameters_human_readable_string(self, parameters):
		return f"""Год {parameters['year']} Месяц {parameters['month']}"""

	def get_data_source(self, parameters, current_user_id:int):
		return data_sourses.Points_WithOut_Displays(parameters)

	def get_report_history_information(self, parameters:dict) -> list :
		result = []
		result.append(f'Идентификатор результата: {parameters["id"]}')
		result.append(f'Год: {parameters["year"]}')
		result.append(f'Месяц: {parameters["month"]}')
		result.append(f'Время формирования: {parameters["dt"]:%Y-%m-%d %H:%M}')
		return result

	def __str__(self):
		return str(self.dialog)


class Points_with_Constant_Consuming(Report):
	def __init__(self):
		self.report_name = 'Report_Points_with_Constant_Consuming'
		self.report_humanread_name = get_human_readable_report_name(self.report_name)
		self.dialog = dialogs.DialogParameters(title=get_human_readable_report_name(self.report_name), backlink=f'/RunReport/{self.report_name}')
		self.dialog.add_months('Месяц','month')
		self.dialog.add_years('Год','year')
		self.get_data_source_procedure_name = 'data_sourses.Points_with_Constant_Consuming'
		#self.dialog.add_checkbox('Открыть последний отчет от этих параметров','last',0)

	def get_parameters_human_readable_string(self, parameters):
		return f"""Год {parameters['year']} Месяц {parameters['month']}"""

	def get_data_source(self, parameters, current_user_id:int):
		return data_sourses.Points_with_Constant_Consuming(parameters)

	def get_report_history_information(self, parameters:dict) -> list :
		result = []
		result.append(f'Идентификатор результата: {parameters["id"]}')
		result.append(f'Год: {parameters["year"]}')
		result.append(f'Месяц: {parameters["month"]}')
		result.append(f'Время формирования: {parameters["dt"]:%Y-%m-%d %H:%M}')
		return result

	def __str__(self):
		return str(self.dialog)


class Points_Heads_And_Submissives(Report):
	def __init__(self):
		self.report_name = 'Points_Heads_And_Submissives'
		self.report_humanread_name = get_human_readable_report_name(self.report_name)
		self.dialog = dialogs.DialogParameters(title=get_human_readable_report_name(self.report_name), backlink=f'/RunReport/{self.report_name}')
		self.dialog.add_months('Месяц','month')
		self.dialog.add_years('Год','year')

	def get_parameters_human_readable_string(self, parameters):
		return f"""Год {parameters['year']} Месяц {parameters['month']}"""

	def get_data_source(self, parameters, current_user_id:int):
		return data_sourses.Get_Data_For_Report_Heads_and_Submissives(parameters)

	def get_report_history_information(self, parameters:dict) -> list :
		result = []
		result.append(f'Идентификатор результата: {parameters["id"]}')
		result.append(f'Год: {parameters["year"]}')
		result.append(f'Месяц: {parameters["month"]}')
		result.append(f'Время формирования: {parameters["dt"]:%Y-%m-%d %H:%M}')
		return result

	def __str__(self):
		return str(self.dialog)



class Pays_from_date_to_date(Report):
	def __init__(self):
		self.report_name = 'Report_pays_from_date_to_date'
		self.report_humanread_name = get_human_readable_report_name(self.report_name)
		self.dialog = dialogs.DialogParameters(title=get_human_readable_report_name(self.report_name), backlink=f'/RunReport/{self.report_name}') #backlink=f'/RunReport/{self.report_name}
		self.dialog.add_date('С', 'from', datetime.date.today().replace(day=1).isoformat())
		self.dialog.add_date('По', 'to', last_day_of_month(datetime.date.today()).isoformat())
		self.dialog.success_code=''
		self.get_data_source_procedure_name = 'data_sourses.Pays_from_date_to_date'

	def get_parameters_human_readable_string(self, parameters):
		return f"""с {parameters['from']} ПО {parameters['to']}"""

	def get_data_source(self, parameters, current_user_id:int):
		return data_sourses.Pays_from_date_to_date(parameters)

	def get_report_history_information(self, parameters:dict) -> list :
		result = []
		result.append(f'Идентификатор результата: {parameters["id"]}')
		result.append(f'C: {parameters["from"]}')
		result.append(f'ПО: {parameters["to"]}')
		result.append(f'Время формирования: {parameters["dt"]:%Y-%m-%d %H:%M}')
		return result

	def __str__(self):
		return str(self.dialog)


# adapter for dictionary of report objects
class Reports:
	def __init__(self):
		self.reports: dict[str, Report] = {}

	def add(self, oreport:Points_WithOut_Displays):
		self.reports[oreport.report_name] = oreport
		pass
	
	def report_names_list(self):
		result = []
		for key, _ in self.reports.items():
			result.append(key)
		return result

	def __str__(self):
		result = ''
		for key, value in self.reports.items():
			result += f"{key}:{value.dialog}\n"
		return result


