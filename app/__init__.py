import logging
from logging.handlers import RotatingFileHandler
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#from flask_migrate import Migrate
from flask_login import LoginManager
#from flask_mail import Mail
from config import Config, connection_url_ul, connection_url_fl
import pprint
from sqlalchemy import create_engine

printer = pprint.PrettyPrinter(indent=12, width=160)
prnt = printer.pprint    


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)


engine_ul = create_engine(connection_url_ul)
engine_fl = create_engine(connection_url_fl)
connection_ul = engine_ul.connect()
connection_fl = engine_fl.connect()



login = LoginManager(app)
login.login_view = 'login'


if not os.path.exists('logs'):
    os.mkdir('logs')
file_handler = RotatingFileHandler('logs/AISpy.log', maxBytes=10240,
                                    backupCount=10)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
file_handler.setLevel( logging.INFO)
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)
app.logger.info('AISpy startup')

#from app import routes, models, errors
from app import routes,  models


