import os
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

echo(style(text=connection_url_fl, bg='blue', fg='bright_green'))
echo(style(text=connection_url_ul, bg='blue', fg='bright_green'))




basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
	SECRET_KEY = config["engine"]["SECRET_KEY"] #os.environ.get('SECRET_KEY') or 'you-will-never-guess'
	SQLALCHEMY_DATABASE_URI = f'{config["login"]["ENGINE"]}://{config["login"]["USERNAME"]}:{config["login"]["PASSWORD"]}@{config["login"]["SERVER"]}:{config["login"]["PORT"]}/{config["login"]["DATABASE"]}'
	echo(style(text=SQLALCHEMY_DATABASE_URI, bg='blue', fg='bright_green'))
	SQLALCHEMY_BINDS = {
		'dbfl': connection_url_fl,
		'dbul': connection_url_ul
}
	TEMPLATES_AUTO_RELOAD = True
