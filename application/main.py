import sys
from click import echo, style

applicaton_mode = (('flask' if __name__ == '__main__' and sys.argv[1]=='flask' else ('celery' if sys.argv[1]!='flask' else 'flask')))

print(f"sys.argv[1]={sys.argv[1]}")

if __name__ == '__main__' and sys.argv[1]=='flask':
	print({"message":"flask init"})
	from common import app
	from endpoints import *
	import logging

	stdout_handler = logging.StreamHandler(sys.stdout)
	stdout_handler.setLevel(logging.ERROR)
	app.logger.addHandler(stdout_handler)
	app.run(host='0.0.0.0', port=sys.argv[2], debug=True, use_reloader=True)

if sys.argv[1]!='flask':
	print({"message":"celery init"})
	import designerUL
	import statements
	from celery import Celery
	celery = Celery('AISpy',broker='amqp://guest:guest@localhost/', backend='rpc://')
	from common import app
	app.config['SERVER_NAME'] = 'mock.com'
	app.config['APPLICATION_ROOT'] = '/'
	app.config['PREFERRED_URL_SCHEME'] = 'http'

	# from kombu import serialization
	# import pickle
	# serialization.register('pickle', pickle.dumps, pickle.loads, content_type='application/x-python-serialize')
	# celery.conf.update(CELERY_ACCEPT_CONTENT=['pickle'])
	
