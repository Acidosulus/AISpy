from celery import Celery
import time
import asyncio

# Создание экземпляра Celery с указанием бэкенда
app = Celery('tasks',
				broker='amqp://guest:guest@localhost',
				task_always_eager=True)
# Определение задачи
@app.task
def add(x, y):
	return x + y


async def main():
	# Вызов задачи
	result = add.delay(4, 4)

	while result.status!='SUCCESS':
		print(result.status)
		print(type(result.status))
	print(result.status)
	return result.result

if __name__ == '__main__':
	print(asyncio.run(main()))