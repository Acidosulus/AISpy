import time
from celery import Celery

app = Celery('myapp', broker='pyamqp://guest@localhost//')

@app.task
def generate_report_task(arg1, arg2):
	print("Start generating report")
	time.sleep(10)
	print("Report generated")
	
generate_report_task.apply_async(args=[1], kwargs={'key': 'value'})
