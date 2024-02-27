from celery import Celery

app = Celery('tasts', broker='pyamqp://guest@localhost//')

def add(x,y):
	return x +y