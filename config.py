"# Файл конфигурации для подключения к базе данных
# Настройки подключения к базе данных
# Автор: Mih10

import psycopg2

def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname="mih10",
            user="postgres",
            password="123",
            host="127.0.0.1",
            port="5432"
        )
        print("Подключение к базе данных установлено")
        return conn
    except Exception as e:
        print(f"Ошибка при подключении к базе данных: {e}")
        return None
