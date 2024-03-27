import app.designerUL

from celery import Celery
celery = Celery('AISpy',broker='amqp://guest:guest@localhost//', backend='rpc://')
from celery import current_task

from celery.result import AsyncResult


@celery.task(name='app.designerUL.Data_Construct')
def Data_Construct(current_user_id, csource:str, cparameters:str):
	result = app.designerUL.Data_Construct(current_user_id, csource, cparameters)
	return result




