from datetime import datetime, timezone
from urllib.parse import urlsplit
from flask import render_template, flash, redirect, url_for, request
import sqlalchemy as sa
from collections.abc import Iterable
from app import app, db, models,connection_fl

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
									Null);""")
	pItem = models.PageItemsList(   name='Рассчитанность ТУ МКЖД',
									path='/Report/Report_Calc_Status_MKJD_Point',
									icon='/static/images/ico_excel.bmp',
									roles='0',
									persistent_id=1901)

	db.session.add(pItem)
	db.session.commit()
	return redirect(url_for('index'))



@app.route('/reports/')
def reports():
	prnt(RowsToDictList(db.session.query(models.PageItemsList).all()))
	reportsList = RowsToDictList(db.session.query(models.PageItemsList).all())
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

