from flask import Flask, render_template
import os
from flask_sqlalchemy import SQLAlchemy
import pymssql
import urllib
from click import echo, style
import configparser  # импортируем библиотеку

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'a really really really really long secret key'

#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:321@185.112.225.153:35432/start_dev'
config = configparser.ConfigParser()
config.read("settings.ini", encoding='UTF-8')  

app.config['SQLALCHEMY_DATABASE_URI'] = f'mssql+pymssql://{urllib.parse.quote_plus("КАЗАКОВЦЕВ_НМ")}:{urllib.parse.quote_plus("1")}@{urllib.parse.quote_plus("10.19.50.11:1433")}/{urllib.parse.quote_plus("atom_khk_ul.stack")}'
db = SQLAlchemy(app)



def root_dir():  # pragma: no cover
    return os.path.abspath(os.path.dirname(__file__))


def get_file(filename):  # pragma: no cover
    try:
        src = os.path.join(root_dir(), filename)
        # Figure out how flask returns static files
        # Tried:
        # - render_template
        # - send_file
        # This should not be so non-obvious
        return open(src).read()
    except IOError as exc:
        return str(exc)


@app.route('/')
@app.route('/index')
def index():
    user = {'nickname':'UserName'}
    title = 'AISpy'
    return render_template("main_index.html", title = title, user = user)



if __name__ == "__main__":
    app.run()