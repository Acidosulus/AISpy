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
	app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=True)

if sys.argv[1]!='flask':
	print({"message":"celery init"})
	import designerUL
	from celery import Celery
	celery = Celery('AISpy',broker='amqp://guest:guest@localhost//', backend='rpc://')
	
