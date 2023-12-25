from datetime import datetime, timezone
from urllib.parse import urlsplit
from flask import render_template, flash, redirect, url_for, request
from app import app, db, models,connection_fl, dialogs, common
from click import echo, style
import pprint
from sqlalchemy import text
from app.models import Users
from flask_login import login_user, logout_user, current_user
printer = pprint.PrettyPrinter(indent=12, width=180)
prnt = printer.pprint



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


@app.route('/Report/<report_name>')
def Report(report_name):
	echo(style(text='Report:', fg='black', bg='white') + ' ' + style(text=report_name, fg='bright_white'))
	return redirect(url_for('index'))


@app.route('/RunReport/<report_name>', methods=['POST'])
def RunReport(report_name):
	echo(style(text='Report:', fg='black', bg='white') + ' ' + style(text=report_name, fg='bright_white'))
	echo(style('dialog answer: ', fg='yellow')+style(dialogs.testdialog.get_answers(request.form.items()), fg='bright_yellow'))
	return redirect(url_for('index'))


@app.route('/addresses/<object_id>')
def addresses(object_id):
	print(object_id)
	results = Get_Addresses_List(object_id)
	print('=============================')
	prnt(results)
	print('=============================')
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

	db.engine.connect().execute(text("""insert into page_items_list (name, path, icon, roles, persistent_id, parent) 
									values('ТУ не имеющие показаний в текущем расчётном периоде',
									'/Report/Points_WithOut_Displays',
									'/static/images/ico_excel.bmp',
									'0',
									1900,
									-110);"""))
	
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
	rows = common.RowsToDictList(db.session.query(models.PageItemsList).filter(models.PageItemsList.parent==parent_id).all())
	prnt(rows)
	print()
	for row in rows:
		if len(row['path'])==0:
			row['path'] = f'/page_with_items/{row["persistent_id"]}'
	prnt(rows)
	reportsList = rows
	return render_template("reports_index.html", reports=reportsList)


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = Users(username=request.form.get("username"),
                     password=request.form.get("password"))
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("register"))
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











