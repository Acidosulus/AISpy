from datetime import datetime, timezone
from urllib.parse import urlsplit
from flask import render_template, flash, redirect, url_for, request
import sqlalchemy as sa
from app import app, db


@app.route('/')
@app.route('/index')
def index():
    user = {'nickname':'UserName'}
    title = 'AISpy'
    return render_template("main_index.html", title = title, user = user)