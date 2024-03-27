import sys
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from common import connection_url_ul, connection_url_fl
#from flask_celery import Celery
import pprint
from endpoints import *
printer = pprint.PrettyPrinter(indent=12, width=160)
prnt = printer.pprint
from click import echo, style


from celery import Celery, Task
from common import app





class CallbackTask(Task, metaclass=type):
    def on_success(self, retval, task_id, args, kwargs):
        echo(style(text=f"Задача {task_id} выполнена успешно!", fg='bright_red'))

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        echo(style(text=f"Задача {task_id} завершилась с ошибкой: {exc}", fg='bright_red'))



if __name__ == '__main__' and sys.argv[1]=='flask':
	prnt({"message":"flask init"})
	app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=True)
else:
	prnt({"message":"celery init"})
	celery = Celery('AISpy',broker='amqp://guest:guest@localhost//', backend='rpc://')

	
	@celery.task(name='app.designerUL.Data_Construct', base=CallbackTask)
	def Data_Construct(current_user_id, csource:str, cparameters:str):
		import designerUL
		result = designerUL.Data_Construct(current_user_id, csource, cparameters)
		return result
