from datetime import datetime, timezone
from urllib.parse import urlsplit
from flask import render_template, flash, redirect, url_for, request
import sqlalchemy as sa
from app import app, db, models


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


@app.route('/reports/')
def reports():
    reportsList = [{'name':'Первый отчёт', 'add_link':'report1'}, {'name':'Второй отчёт', 'add_link':'report2'}, {'name':'Третий отчет', 'add_link':'report3'}]
    return render_template("reports_index.html", reports=reportsList)






