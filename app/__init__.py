import logging
from logging.handlers import RotatingFileHandler
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#from flask_migrate import Migrate
from flask_login import LoginManager, login_user
#from flask_mail import Mail
from config import Config, connection_url_ul, connection_url_fl
from sqlalchemy import create_engine
#from flask_celery import Celery

import pprint
printer = pprint.PrettyPrinter(indent=12, width=160)
prnt = printer.pprint    


app = Flask(__name__)
app.config.from_object(Config)

app.TMP_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'tmp')

#celery = Celery('tasks',
#				broker='amqp://guest:guest@localhost',
#				task_always_eager=True)


db = SQLAlchemy(app)
with app.app_context():
	connection = db.engine.connect()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'




engine_ul = create_engine(connection_url_ul)
engine_fl = create_engine(connection_url_fl)
connection_ul = engine_ul.connect()
connection_fl = engine_fl.connect()





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




from app import statements

with app.app_context():

	pull = statements.Reports()
	pull.add(statements.Points_WithOut_Displays())
	pull.add(statements.Points_with_Constant_Consuming())
	pull.add(statements.Pays_from_date_to_date())

#	print('Registred reports:')
#	print(pull)

from app import routes,  models