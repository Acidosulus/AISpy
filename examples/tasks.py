from celery import Celery

# Создание экземпляра Celery
app = Celery('tasks', broker='amqp://guest:guest@localhost')

# Определение задачи
@app.task
def add(x, y):
    return x + y
