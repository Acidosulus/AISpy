from collections.abc import Iterable
from dataclasses import dataclass
from celery import Task
import uuid
import logging
from logging.handlers import RotatingFileHandler


from celery import Celery
celery = Celery('data_sourses',broker='amqp://guest:guest@localhost/', backend='rpc://')
from celery import current_task
# from kombu import serialization
# import pickle
# serialization.register('pickle', pickle.dumps, pickle.loads, content_type='application/x-python-serialize')
# celery.conf.update(CELERY_ACCEPT_CONTENT=['pickle'])



class Celery_Task():
	def __init__(self, task:Task, user_id:int, type:str):
		self.task = task
		self.id = str(uuid.uuid4())
		self.user_id = user_id
		self.type = '' #file_download - task return path for file. The file must by downloaded from browser. Link on file must be put into browser event log
		self.active = True

	def Information(self):
		return {'task:':self.task, 'id:':self.id, 'user_id:':self.user_id, 'ready:':self.task.ready()} # 'result:':self.task.get()

class Celery_Tasks_Pull():
	pull={}

	def __init__(self):
		pass

	def add_task(self, task:Task, user_id:int, type):
		celery_task = Celery_Task(task, user_id, type)
		self.pull[celery_task.id] = celery_task
		return celery_task

# return one row query result as dict
def RowToDict(row):
	# result = {}
	# for column in row.__table__.columns:
	# 	result[column.name] = str(getattr(row, column.name))
	return row._asdict()

# returl query result as dict list
def RowsToDictList(results):
	# так хорошо, нужно лишь решить проблему с NoneTypes
	list_of_dicts = []
	for result in results:
		dict_entry = {}
		for column in result.__table__.columns:
			dict_entry[column.name] = getattr(result, column.name)
		list_of_dicts.append(dict_entry)

	print(list_of_dicts)
	return list_of_dicts

	print(rows)
	print()
	prnt(rows)
	if rows is None:
		return [{}]
	result = []
	for row in rows:
		dic = {}
		print('=================================================================================================')
		if isinstance(row, Iterable):
			for element in row:
				print(RowToDict(element))
				dic = {**dic, **RowToDict(element)}
			result.append(dic)
		else:
			print(element)
			prnt(element)
			print(RowToDict(element))
			result.append(RowToDict(row))
		print('=================================================================================================')
	return result


@dataclass
class Navbar_Button:
	href: str
	title: str
	src: str
	onclick: str


class Button_Home(Navbar_Button):
	def __init__(self, href='/', title='В начало', src='home.png', onclick=''):
		self.href = href
		self.title = title
		self.src = src
		self.onclick = onclick

		

class Button_Back(Navbar_Button):
	def __init__(self, href='', title='Назад', src='back.png', onclick='javascript:history.back(); return false;'):
		self.href = href
		self.title = title
		self.src = src
		self.onclick = onclick


class Button_List(Navbar_Button):
	def __init__(self, href='', title='Список ранее сформированных отчетов', src='list.png', onclick=''):
		self.href = href
		self.title = title
		self.src = src
		self.onclick = onclick


class Button_Excel(Navbar_Button):
	def __init__(self, href='', title='Скачать отчет Excel', src='excel.png', onclick=''):
		self.href = href
		self.title = title
		self.src = src
		self.onclick = onclick


class Agreements_Search(Navbar_Button):
	def __init__(self, href='', title='Поиск договоров', src='lupe.png', onclick='RunInScreenForm(`agreements_search`, `FillOutOrganizationForm();`, `/agreement_search_form`);'):
		self.href = href
		self.title = title
		self.src = src
		self.onclick = onclick


from flask import Flask
from sqlalchemy import create_engine
import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager, login_user

basedir = os.path.abspath(os.path.dirname(__file__))
import configparser  # импортируем библиотеку
import pprint
from click import echo, style

printer = pprint.PrettyPrinter(indent=12, width=180)
prnt = printer.pprint

config = configparser.ConfigParser()
config.read("settings.ini", encoding='UTF-8')  

from sqlalchemy.engine import URL

connection_url_fl = URL.create(
	config['login_fl']['ENGINE'],
	username=config['login_fl']['USERNAME'],
	password=config['login_fl']['PASSWORD'],
	host=config['login_fl']['SERVER'],
	port=config['login_fl']['PORT'],
	database=config['login_fl']['DATABASE'],
	query={
		"driver": config['login_fl']['DRIVER'],
		"TrustServerCertificate": "yes",
		"extra_params": "MARS_Connection=Yes"	},
)
connection_url_ul = URL.create(
	config['login_ul']['ENGINE'],
	username=config['login_ul']['USERNAME'],
	password=config['login_ul']['PASSWORD'],
	host=config['login_ul']['SERVER'],
	port=config['login_ul']['PORT'],
	database=config['login_ul']['DATABASE'],
	query={
		"driver": config['login_ul']['DRIVER'],
		"TrustServerCertificate": "yes",
		"extra_params": "MARS_Connection=Yes"	},
)

# echo(style(text=connection_url_fl, bg='blue', fg='bright_green'))
# echo(style(text=connection_url_ul, bg='blue', fg='bright_green'))



basedir = os.path.abspath(os.path.dirname(__file__))

# class Config:
SECRET_KEY = config["engine"]["SECRET_KEY"] #os.environ.get('SECRET_KEY') or 'you-will-never-guess'
SQLALCHEMY_DATABASE_URI = f'{config["login"]["ENGINE"]}://{config["login"]["USERNAME"]}:{config["login"]["PASSWORD"]}@{config["login"]["SERVER"]}:{config["login"]["PORT"]}/{config["login"]["DATABASE"]}'
# 	echo(style(text=SQLALCHEMY_DATABASE_URI, bg='blue', fg='bright_green'))
# 	SQLALCHEMY_BINDS = {
# 		'dbfl': connection_url_fl,
# 		'dbul': connection_url_ul
# 	}
# 	TEMPLATES_AUTO_RELOAD = True
	
app = Flask(__name__)
# app.config.from_object(Config)
app.TMP_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'tmp')
app.config['SQLALCHEMY_DATABASE_URI']=SQLALCHEMY_DATABASE_URI
app.config['SECRET_KEY']=SECRET_KEY
db = SQLAlchemy(app)

engine_ul = create_engine(connection_url_ul)
engine_fl = create_engine(connection_url_fl)
from sqlalchemy.orm import Session
session_ul = Session(engine_ul)
connection_ul = engine_ul.connect()
connection_fl = engine_fl.connect()
with app.app_context():
	connection = db.engine.connect()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

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


#celery = Celery('tasks',
#				broker='amqp://guest:guest@localhost',
#				task_always_eager=True)




