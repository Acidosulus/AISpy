import sys

class ConsoleFilter:
    def __init__(self):
        self.stdout = sys.stdout
        self.stderr = sys.stderr

    def write(self, msg):
        if 'INFO:werkzeug:' not in msg:
            self.stdout.write(msg)

    def flush(self):
        self.stdout.flush()

# Перенаправляем вывод в экземпляр класса ConsoleFilter
sys.stdout = ConsoleFilter()
sys.stderr = ConsoleFilter()

# Пример использования
if __name__ == "__main__":
    print("Это сообщение будет выведено")
    print("INFO:werkzeug: Это сообщение не будет выведено")
    print("Еще одно сообщение для проверки")
