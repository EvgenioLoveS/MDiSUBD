import datetime
from db import connect_db

def employee_menu():
    while True:
        print("\n" + "="*40)
        print("                Меню сотрудника")
        print("="*40)
        print("1. Управлять товарами")
        print("2. Управлять категориями")
        print("3. Управлять скидками")
        print("4. Просматривать информацию о клиентах")
        print("5. Просматривать логи клиентов")
        print("6. Просматривать информацию о заказах") 
        print("7. Выйти в главное меню")
        print("="*40)

        choice = input("Выберите опцию (1-7): ")

        if choice == '1':
            manage_products()
        elif choice == '2':
            manage_categories()
        elif choice == '3':
            manage_discounts()
        elif choice == '4':  
            view_clients()
        elif choice == '5':  
            view_clients_logs()
        elif choice == '6':
            view_orders()
        elif choice == '7':
            print("\n🔙 Возврат в главное меню.")
            break
        else:
            print("\n❌ Неверный выбор. Пожалуйста, выберите опцию от 1 до 7.")
            print("-" * 40)

def manage_products():
    while True:
        print("\n" + "="*40)
        print("            Управление товарами")
        print("="*40)
        print("1. Добавить новый товар")
        print("2. Просмотреть список товаров")
        print("3. Изменить товар")
        print("4. Удалить товар")
        print("5. Выйти")
        print("="*40)

        choice = input("Выберите опцию (1-5): ")

        if choice == '1':
            add_product()
        elif choice == '2':
            view_products()
        elif choice == '3':
            update_product()
        elif choice == '4':
            delete_product()
        elif choice == '5':
            break
        else:
            print("\n❌ Неверный выбор. Пожалуйста, выберите опцию от 1 до 5.")
            print("-" * 40)


def add_product():
    """Функция для добавления нового товара."""
    # Вывод списка категорий
    view_categories()

    connection = connect_db()
    cursor = connection.cursor()
    try:
        name = input("\nВведите название товара: ")
        category_id = int(input("Введите ID категории товара (см. список выше): "))
        price = float(input("Введите цену товара: "))
        quantity = int(input("Введите количество товара: "))
        brand = input("Введите бренд товара: ")
        production_date = input("Введите дату производства (YYYY-MM-DD): ")
        description = input("Введите описание товара: ")

        cursor.execute("""
            INSERT INTO product 
            (name, product_category_id, price, quantity, brand, production_date, description)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (name, category_id, price, quantity, brand, production_date, description))
        connection.commit()
        print("\n✅ Товар успешно добавлен.")
    except Exception as e:
        print(f"\n❌ Ошибка при добавлении товара: {e}")
    finally:
        cursor.close()
        connection.close()


def view_products():
    connection = connect_db()
    cursor = connection.cursor()
    try:
        # SQL-запрос для получения нужных полей из таблицы product
        cursor.execute("""
            SELECT 
                product_id,
                product_category_id,
                price,
                name,
                production_date,
                quantity,
                brand,
                description
            FROM 
                product
        """)
        products = cursor.fetchall()

        # Задаем заголовки колонок вручную
        column_names = [
            "product_id", 
            "product_category_id", 
            "price", 
            "name", 
            "production_date", 
            "quantity", 
            "brand", 
            "description"
        ]

        # Вывод названий колонок
        print("\n📦 Список товаров:")
        print(" | ".join(column_names))

        # Вывод значений
        for product in products:
            print(" | ".join(str(value) if value is not None else "NULL" for value in product))
    except Exception as e:
        print(f"\n❌ Ошибка при выводе списка товаров: {e}")
    finally:
        cursor.close()
        connection.close()

def update_product():
    view_products()  # Показываем список товаров
    connection = connect_db()
    cursor = connection.cursor()
    try:
        product_id = input("\nВведите ID товара для изменения: ")
        column = input("Введите название колонки для изменения (name, price, quantity, brand_id, product_category_id): ")
        new_value = input("Введите новое значение: ")

        # Проверка на число (если редактируется price или quantity)
        if column in ["price", "quantity", "brand_id", "product_category_id"]:
            new_value = int(new_value)

        cursor.execute(f"UPDATE product SET {column} = %s WHERE product_id = %s", (new_value, product_id))
        connection.commit()
        print("\n✅ Товар успешно обновлен.")
    except Exception as e:
        print(f"\n❌ Ошибка при обновлении товара: {e}")
    finally:
        cursor.close()
        connection.close()


def delete_product():
    view_products()  # Показываем список товаров
    connection = connect_db()
    cursor = connection.cursor()
    try:
        product_id = input("\nВведите ID товара для удаления: ")

        cursor.execute("DELETE FROM product WHERE product_id = %s", (product_id,))
        connection.commit()
        print("\n✅ Товар успешно удален.")
    except Exception as e:
        print(f"\n❌ Ошибка при удалении товара: {e}")
    finally:
        cursor.close()
        connection.close()




def manage_categories():
    while True:
        print("\n" + "="*40)
        print("          Управление категориями")
        print("="*40)
        print("1. Добавить новую категорию")
        print("2. Просмотреть список категорий")
        print("3. Изменить категорию")
        print("4. Удалить категорию")
        print("5. Выйти")
        print("="*40)

        choice = input("Выберите опцию (1-5): ")

        if choice == '1':
            add_category()
        elif choice == '2':
            view_categories()
        elif choice == '3':
            update_category()
        elif choice == '4':
            delete_category()
        elif choice == '5':
            break
        else:
            print("\n❌ Неверный выбор. Пожалуйста, выберите опцию от 1 до 5.")
            print("-" * 40)

def add_category():
    connection = connect_db()
    cursor = connection.cursor()
    try:
        name = input("Введите название категории: ")
        cursor.execute("INSERT INTO product_category (name) VALUES (%s)", (name,))
        connection.commit()
        print("\n✅ Категория успешно добавлена.")
    except Exception as e:
        print(f"\n❌ Ошибка при добавлении категории: {e}")
    finally:
        cursor.close()
        connection.close()

def view_categories():
    connection = connect_db()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM product_category")
        categories = cursor.fetchall()
        print("\n📂 Список категорий:")
        for category in categories:
            print(f"ID: {category[0]}, Название: {category[1]}")
    except Exception as e:
        print(f"\n❌ Ошибка при выводе списка категорий: {e}")
    finally:
        cursor.close()
        connection.close()

def update_category():
    connection = connect_db()
    cursor = connection.cursor()
    try:
        print("\n📂 Доступные категории:")
        view_categories()  # Показываем список категорий

        category_id = input("\nВведите ID категории для изменения: ")
        new_name = input("Введите новое название категории: ")

        cursor.execute("UPDATE product_category SET name = %s WHERE product_category_id = %s", (new_name, category_id))
        connection.commit()
        print("\n✅ Категория успешно обновлена.")
    except Exception as e:
        print(f"\n❌ Ошибка при обновлении категории: {e}")
    finally:
        cursor.close()
        connection.close()


def delete_category():
    connection = connect_db()
    cursor = connection.cursor()
    try:
        print("\n📂 Доступные категории:")
        view_categories()  # Показываем список категорий

        category_id = input("\nВведите ID категории для удаления: ")
        cursor.execute("DELETE FROM product_category WHERE product_category_id = %s", (category_id,))
        connection.commit()
        print("\n✅ Категория успешно удалена.")
    except Exception as e:
        print(f"\n❌ Ошибка при удалении категории: {e}")
    finally:
        cursor.close()
        connection.close()


def manage_discounts():
    while True:
        print("\n" + "="*40)
        print("           Управление скидками")
        print("="*40)
        print("1. Добавить новую скидку")
        print("2. Просмотреть список скидок")
        print("3. Изменить скидку")
        print("4. Удалить скидку")
        print("5. Выйти")
        print("="*40)

        choice = input("Выберите опцию (1-5): ")

        if choice == '1':
            add_discount()
        elif choice == '2':
            view_discounts()
        elif choice == '3':
            update_discount()
        elif choice == '4':
            delete_discount()
        elif choice == '5':
            break
        else:
            print("\n❌ Неверный выбор. Пожалуйста, выберите опцию от 1 до 5.")
            print("-" * 40)


def add_discount():
    connection = connect_db()
    cursor = connection.cursor()
    try:
        name = input("\nВведите название скидки: ")
        description = input("Введите описание скидки: ")
        percent = int(input("Введите процент скидки: "))
        is_active = input("Скидка активна? (yes/no): ").lower() == "yes"

        cursor.execute("""
            INSERT INTO discount (name, description, percent, is_active) 
            VALUES (%s, %s, %s, %s)
        """, (name, description, percent, is_active))
        connection.commit()
        print("\n✅ Скидка успешно добавлена.")
    except Exception as e:
        print(f"\n❌ Ошибка при добавлении скидки: {e}")
    finally:
        cursor.close()
        connection.close()


def view_discounts():
    """Функция для просмотра списка скидок."""
    connection = connect_db()
    cursor = connection.cursor()
    try:
        # SQL-запрос для получения всех полей из таблицы discount
        cursor.execute("""
            SELECT 
                discount_id,
                description,
                name,
                percent,
                is_active
            FROM 
                discount
        """)
        discounts = cursor.fetchall()

        # Задаем заголовки колонок
        column_names = [
            "discount_id", 
            "description", 
            "name", 
            "percent", 
            "is_active"
        ]

        # Вывод заголовков таблицы
        print("\n🎁 Список скидок:")
        print(" | ".join(column_names))
        print("-" * 50)

        # Вывод данных о скидках
        for discount in discounts:
            print(" | ".join(
                str(value) if value is not None else "NULL" 
                for value in discount
            ))
    except Exception as e:
        print(f"\n❌ Ошибка при выводе списка скидок: {e}")
    finally:
        cursor.close()
        connection.close()

def update_discount():
    connection = connect_db()
    cursor = connection.cursor()
    try:
        print("\n🎁 Доступные скидки:")
        view_discounts()  # Показываем список скидок

        discount_id = input("\nВведите ID скидки для изменения: ")
        column = input("Введите название колонки для изменения (name, description, percent, is_active): ")
        new_value = input("Введите новое значение: ")

        # Проверка на тип данных (для процента и активности)
        if column == "percent":
            new_value = int(new_value)
        elif column == "is_active":
            new_value = new_value.lower() == "yes"

        cursor.execute(f"UPDATE discount SET {column} = %s WHERE discount_id = %s", (new_value, discount_id))
        connection.commit()
        print("\n✅ Скидка успешно обновлена.")
    except Exception as e:
        print(f"\n❌ Ошибка при обновлении скидки: {e}")
    finally:
        cursor.close()
        connection.close()


def delete_discount():
    connection = connect_db()
    cursor = connection.cursor()
    try:
        print("\n🎁 Доступные скидки:")
        view_discounts()  # Показываем список скидок

        discount_id = input("\nВведите ID скидки для удаления: ")
        cursor.execute("DELETE FROM discount WHERE discount_id = %s", (discount_id,))
        connection.commit()
        print("\n✅ Скидка успешно удалена.")
    except Exception as e:
        print(f"\n❌ Ошибка при удалении скидки: {e}")
    finally:
        cursor.close()
        connection.close()


def view_clients():
    """Функция для просмотра информации о клиентах."""
    connection = connect_db()
    cursor = connection.cursor()
    try:
        cursor.execute("""
            SELECT 
                client_id, 
                first_name, 
                last_name, 
                phone, 
                email 
            FROM 
                client
        """)
        clients = cursor.fetchall()

        print("\n👤 Информация о клиентах:\n")
        if clients:
            # Вывод информации о каждом клиенте
            for client in clients:
                print(f"ID: {client[0]}")
                print(f"Имя: {client[1]}")
                print(f"Фамилия: {client[2]}")
                print(f"Телефон: {client[3]}")
                print(f"Email: {client[4]}")
                print("-" * 20)  # Разделитель между клиентами
        else:
            print("Данные о клиентах отсутствуют.")
    except Exception as e:
        print(f"\n❌ Ошибка при выводе информации о клиентах: {e}")
    finally:
        cursor.close()
        connection.close()


def view_orders():
    connection = connect_db()
    cursor = connection.cursor()
    try:
        # SQL-запрос для получения информации о заказах
        cursor.execute("""
            SELECT 
                o.order_id,
                o.client_id,
                o.date AS order_date,
                o.price AS total_price,
                c.first_name AS client_first_name,
                c.last_name AS client_last_name
            FROM 
                "order" o
            JOIN 
                client c ON o.client_id = c.client_id
        """)
        orders = cursor.fetchall()

        # Задаем заголовки колонок
        column_names = [
            "order_id", 
            "client_id", 
            "order_date", 
            "total_price", 
            "client_first_name", 
            "client_last_name"
        ]

        # Вывод заголовков таблицы
        print("\n📜 Список заказов:")
        print(" | ".join(column_names))
        print("-" * 50)

        # Вывод данных о заказах
        for order in orders:
            print(" | ".join(
                str(value) if value is not None else "NULL" 
                for value in order
            ))
    except Exception as e:
        print(f"\n❌ Ошибка при выводе списка заказов: {e}")
    finally:
        cursor.close()
        connection.close()


def view_clients_logs():
    """Функция для отображения логов клиентов."""
    connection = connect_db()
    cursor = connection.cursor()
    try:
        # SQL-запрос для получения логов с привязкой к клиенту
        cursor.execute("""
            SELECT logs.id, client.first_name, client.last_name, logs.action, logs.timestamp
            FROM logs
            INNER JOIN client ON logs.client_id = client.client_id
            ORDER BY logs.timestamp DESC
        """)
        logs = cursor.fetchall()

        # Вывод заголовков
        print("\n📝 Логи клиентов:")
        print(f"{'ID':<5} {'Имя':<15} {'Фамилия':<15} {'Действие':<30} {'Время':<20}")
        print("-" * 85)

        # Вывод данных о логах
        for log in logs:
            print(f"{log[0]:<5} {log[1]:<15} {log[2]:<15} {log[3]:<30} {log[4]}")
    except Exception as e:
        print(f"\n❌ Ошибка при отображении логов: {e}")
    finally:
        cursor.close()
        connection.close()

