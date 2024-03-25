import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from common import connection_url_ul, connection_url_fl
#from flask_celery import Celery
import pprint
from endpoints import *
printer = pprint.PrettyPrinter(indent=12, width=160)
prnt = printer.pprint    





from common import app






if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=True)



