import app.designerUL

from celery import Celery
celery = Celery('data_sourses',broker='amqp://guest:guest@localhost//', backend='rpc://')
from celery import current_task

@celery.task(name='app.designerUL.Data_Construct')
def Data_Construct(current_user_id, csource:str, cparameters:str):
	return app.designerUL.Data_Construct(current_user_id, csource, cparameters)



