import psycopg2
from psycopg2 import sql

# Устанавливаем соединение с базой данных
def connect_db():
    try:
        connection = psycopg2.connect(
            dbname="InternetShop",
            user="postgres",
            password="1234",
            host="localhost",
            port="5432"
        )
        return connection
    except Exception as e:
        print("Ошибка при подключении к базе данных:", e)
        return None
