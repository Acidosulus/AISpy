from celery import Celery

# Создание экземпляра Celery с указанием бэкенда
app = Celery('tasks',
             broker='amqp://guest:guest@localhost',
             task_always_eager=True)

# Определение задачи
@app.task
def add(x, y):
    return x + y
