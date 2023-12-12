from datetime import datetime, timezone
from urllib.parse import urlsplit
from flask import render_template, flash, redirect, url_for, request
import sqlalchemy as sa
from app import app, db, models
import pprint
printer = pprint.PrettyPrinter(indent=12, width=180)
prnt = printer.pprint


def Get_Addresses_List(parent_id:int) -> list:
    db.engine.connect()
    rez = db.engine.connect().execute(f"select stack.[AddrLs](row_id,0) as address, row_id, Номер as number  from stack.[Лицевые счета] where [Счета]={parent_id};").fetchall()
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


@app.route('/reports/')
def reports():
    reportsList = [{'name':'Первый отчёт', 'add_link':'report1'}, {'name':'Второй отчёт', 'add_link':'report2'}, {'name':'Третий отчет', 'add_link':'report3'}]
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






