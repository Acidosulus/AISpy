from worker import add
import asyncio

async def main():
    # Вызов задачи
    result = add.delay(4, 4)

    while result.status != 'SUCCESS':
        print(result.status)
        print(type(result.status))

    print(result.status)
    return result.result

if __name__ == '__main__':
    print(asyncio.run(main()))
