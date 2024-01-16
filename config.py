import os
basedir = os.path.abspath(os.path.dirname(__file__))
import configparser  # импортируем библиотеку
import urllib
import sys
import pprint
printer = pprint.PrettyPrinter(indent=12, width=180)
prnt = printer.pprint


from sqlalchemy.engine import URL
if sys.platform == 'linux':
	connection_url_fl = URL.create(
		"mssql+pyodbc",
		username="sa",
		password="Bor@Teks",
		host="10.19.50.11",
		port=1433,
		database="atom_khk_fl",
		query={
			"driver": "ODBC Driver 18 for SQL Server",
			"TrustServerCertificate": "yes"	},
	)
	connection_url_ul = URL.create(
		"mssql+pyodbc",
		username="КАЗАКОВЦЕВ_НМ",
		password="1",
		host="10.19.50.11",
		port=1433,
		database="atom_khk_ul_test",
		query={
			"driver": "ODBC Driver 18 for SQL Server",
			"TrustServerCertificate": "yes"	},
	)
else:
	connection_url_fl = URL.create(
		"mssql+pyodbc",
		username="tmpsite",
		password="1",
		host="10.19.50.11",
		port=1433,
		database="atom_khk_fl_testupd",
		query={
			"driver": "SQL Server",
			"TrustServerCertificate": "yes"	},
	)
	connection_url_ul = URL.create(
		"mssql+pyodbc",
		username="КАЗАКОВЦЕВ_НМ",
		password="1",
		host="10.19.50.11",
		port=1433,
		database="atom_khk_ul_test",
		query={
			"driver": "SQL Server",
			"TrustServerCertificate": "yes"	},
	)
print()
prnt(connection_url_fl)
prnt(connection_url_ul)
print()


basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
	config = configparser.ConfigParser()
	config.read("settings.ini", encoding='UTF-8')  
	SECRET_KEY = 'a really really really really long secret key' #os.environ.get('SECRET_KEY') or 'you-will-never-guess'
	SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:321@185.112.225.153:35432/start_dev'
	SQLALCHEMY_BINDS = {
		'dbfl': connection_url_fl,
		'dbul': connection_url_ul
}
	TEMPLATES_AUTO_RELOAD = True
