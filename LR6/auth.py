from db import connect_db

def login_user(email, password):
    connection = connect_db()
    cursor = connection.cursor()
    try:
        cursor.execute("""
            SELECT client_id, first_name, last_name 
            FROM client 
            WHERE email = %s AND password = %s
        """, (email, password))
        user = cursor.fetchone()
        if user:
            print(f"Добро пожаловать, {user[1]} {user[2]}!")  # Вывод приветственного сообщения
            return user[0]  # Возвращаем client_id
        else:
            print("Неверный email или пароль. Попробуйте снова.")  # Сообщение об ошибке авторизации
            return None
    except Exception as e:
        print(f"Ошибка при авторизации клиента: {e}")  # Вывод ошибок базы данных
        return None
    finally:
        cursor.close()
        connection.close()


# Функция для авторизации сотрудника
def login_employee(email, password):
    connection = connect_db()
    cursor = connection.cursor()
    try:
        cursor.execute("""
            SELECT * FROM employee WHERE email = %s AND password = %s
        """, (email, password))
        user = cursor.fetchone()
        if user:
            print(f"Добро пожаловать, сотрудник {user[2]} {user[3]}!")
            return user[0]
        else:
            print("Неверный логин или пароль для сотрудника.")
            return None
    except Exception as e:
        print(f"Ошибка при авторизации сотрудника: {e}")
        return None
    finally:
        cursor.close()
        connection.close()
