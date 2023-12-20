from datetime import datetime, timezone
from urllib.parse import urlsplit
from flask import render_template, flash, redirect, url_for, request
import sqlalchemy as sa
from collections.abc import Iterable
from app import app, db, models,connection_fl
from click import echo, style
import base64
import uuid
import pprint
printer = pprint.PrettyPrinter(indent=12, width=180)
prnt = printer.pprint

# get list of addresses of people with given parent_id
def Get_Addresses_List(parent_id:int) -> list:
	rez = connection_fl.execute(f"select stack.[AddrLs](row_id,0) as address, row_id, Номер as number  from stack.[Лицевые счета] where [Счета]={parent_id};").fetchall()
	result = []
	for element in rez:
		result.append({'address':element[0], 'row_id':element[1], 'number':str(element[2])})
	prnt(result)
	return result


class DialogParameters():
	title = ''
	parameters = []
	def __init__(self, title):
		self.title = title
		self.parameters = []

	def append(self, section):
		self.parameters.append(section)

	def get_answers(self, form_elements):
		result_list = []
		for element in  form_elements:
			result_list.append({element[0]:element[1]})
		return result_list

	def __str__(self) -> str:
		cdata = ''
		for parameter in self.parameters:
			cdata += (', 'if len(cdata)>0 else '') + str(parameter) 
		return '{'+f"title:`{self.title}`,"+'parameters:[' + cdata + ']'+'};'


class DialogSection():
	lable = ''
	type = ''
	default =''
	name = str(uuid.uuid4())
	data = []
	size = '0'
	def __init__(self, lable, type, default, name, data, size,):
		self.lable = lable
		self.name = name
		self.type = type
		self. size = size
		self.default = default
		self.data = data

	def __str__(self) -> str:
		cdata=''
		for element in self.data:
			cdata = cdata + '          '+'{'+f"""id:`{element['id']}`, value:`{element['value']}`"""+'}' #', ' if len(cdata)>0 else ''+
		cdata ='[' + cdata + ']'
		cdata = cdata.replace('}          {','},          {')
		return '{'+f"""lable:`{self.lable}`, name:`{self.name}`, type:`{self.type}`, default:`{self.default}`, size:`{self.size}`, data:{cdata}"""+'}'


dialog = DialogParameters(title='Заголовок диалога с параметрами')
dialog.append( DialogSection(name = 'Первый параметр ввода строки из диалога',
								lable = 'Первый параметр ввода строки из диалога',
								type='edit',
								default='строка по умолчанию',
								data=[],
								size=0) )

dialog.append( DialogSection(name = 'Второй параметр ввода текста из диалога',
								lable = 'Второй параметр ввода текста из диалога',
								type='text',
								default='многострочный\nтекст\nпо\nумолчанию',
								data=[],
								size=0) )

dialog.append( DialogSection(name = 'Третий параметр - флажок',
								lable = 'Третий параметр - флажок',
								type='checkbox',
								default='1',
								data=[],
								size=0) )
dialog.append( DialogSection(name = 'Список значний',
								lable = 'Список значний',
								type='listbox',
								default='1',
								data=[{'id':'1', 'value':'Первое значение'}, {'id':'2', 'value':'Второе значение'}],
								size=0) )



@app.route('/parameters_dialog/')
def parameters_dialog():
	return render_template("parameters_dialog.html", parametesJSON = str(dialog))


@app.route('/Report/<report_name>')
def Report(report_name):
	echo(style(text='Report:', fg='black', bg='white') + ' ' + style(text=report_name, fg='bright_white'))
	return redirect(url_for('index'))


@app.route('/RunReport/<report_name>', methods=['POST'])
def RunReport(report_name):
	echo(style(text='Report:', fg='black', bg='white') + ' ' + style(text=report_name, fg='bright_white'))
	print(dialog.get_answers(request.form.items()))
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

	db.engine.connect().execute("""insert into page_items_list (name, path, icon, roles, persistent_id, parent) 
									values('ТУ не имеющие показаний в текущем расчётном периоде',
									'/Report/Points_WithOut_Displays',
									'/static/images/ico_excel.bmp',
									'0',
									1900,
									-110);""")
	
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






@app.route('/page_with_items/<parent_id>')
def reports(parent_id):
	rows = RowsToDictList(db.session.query(models.PageItemsList).filter(models.PageItemsList.parent==parent_id).all())
	prnt(rows)
	print()
	for row in rows:
		if len(row['path'])==0:
			row['path'] = f'/page_with_items/{row["persistent_id"]}'
	prnt(rows)
	reportsList = rows
	return render_template("reports_index.html", reports=reportsList)






@app.route('/')
@app.route('/index')
def index():
	##### working db insert code ######
	#u = models.User(nickname='john', email='john@email.com', role=models.ROLE_ADMIN)
	#db.session.add(u)
	#db.session.commit()
	##############################
	user = {'nickname':'UserName'}
	title = 'AISpy'
	return render_template("main_index.html", title = title, user = user)





# return one row query result as dict
def RowToDict(row):
	result = {}
	for column in row.__table__.columns:
		result[column.name] = str(getattr(row, column.name))
	return result

# returl query result as dict list
def RowsToDictList(rows):
	if rows is None:
		return [{}]
	result = []
	for row in rows:
		dic = {}
		if isinstance(row, Iterable):
			for element in row:
				dic = {**dic, **RowToDict(element)}
			result.append(dic)
		else:
			result.append(RowToDict(row))
	return result

