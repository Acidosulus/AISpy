from datetime import datetime
from flask import render_template, flash, redirect, url_for, request
from collections.abc import Iterable
from app import app, db, models,connection_fl, dialogs, db, data_sourses
from click import echo, style
import json
import pandas
import xlsxwriter

import pprint
printer = pprint.PrettyPrinter(indent=12, width=180)
prnt = printer.pprint


def get_human_readable_report_name(report_name):
	report_humanread_name = db.engine.execute(db.select(models.PageItemsList.name).where(models.PageItemsList.path==f'/Report/{report_name}')).fetchone()
	try:
		report_humanread_name = report_humanread_name[0]
	except:
		report_humanread_name = ''
	return report_humanread_name



class Points_WithOut_Displays:
	def __init__(self):
		self.report_name = 'ReportPointsWithoutDisplays'
		self.dialog = dialogs.DialogParameters("ТУ не имеющие показаний в текущем расчётном периоде", f'/RunReport/{self.report_name}')
		self.dialog.add_months('Месяц','month')
		self.dialog.add_years('Год','year')

	# return answer for start report with parameters dialog
	def report(self):
		return render_template("parameters_dialog.html", parametesJSON = str(self.dialog), report_name=self.report_name)
	
	# return answer for report_history
	def history(self, user_id):
		report_humanread_name = get_human_readable_report_name(self.report_name)
		rows = db.engine.execute(db.select(models.UserObject.id, models.UserObject.dt, models.UserObject.parameters).where(models.UserObject.user_id == user_id, models.UserObject.name == self.report_name)).fetchall()
		reportsList = []
		for row in rows:
			foo = {}
			foo['path'] = f'/download_excel/{row["id"]}'
			foo['icon'] = f'/static/images/ico_excel.bmp'
			foo['name'] = f'{report_humanread_name} id:{row["id"]} parameters:{row["parameters"]} {row["dt"]:%Y-%m-%d %H:%M}'
			foo['delete_link'] = f"""/delete_report/{row["id"]}"""
			reportsList.append(foo)
		return render_template("reports_index.html", reports=reportsList, list_title = report_humanread_name , list_sub_title = 'история формирования отчёта')

	def run_report(self, parameters, current_user_id):
		header, data = data_sourses.Points_WithOut_Displays(parameters['year'], parameters['month'])
		data_object = models.UserObject(user_id=current_user_id, dt=datetime.now(), name=self.report_name, parameters=json.dumps(parameters, ensure_ascii=False), data=json.dumps(data, ensure_ascii=False))
		db.session.add(data_object)
		db.session.flush()
		data_object_id = data_object.id
		db.session.commit()
		df = pandas.DataFrame(data)
		return render_template("report.html", 
						 	data=df.to_html(classes='table table-success table-striped table-hover table-bordered border-primary align-middle' ), 
							report_title=f"ТУ не имеющие показаний в расчётном периоде {parameters['year']} {parameters['month']}",
							data_object_id=data_object_id,
							report_name = self.report_name)

	def download_excel(self, user_object_id):
		
		pass

	def __str__(self):
		return {self.report_name:self.report_name, 'dialog':str(self.dialog)}

class Reports:
	def __init__(self):
		self.reports = {}

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
	


points_without_displays = Points_WithOut_Displays()

pull = Reports()
pull.add(points_without_displays)

print('Registred reports:')
print(pull)
