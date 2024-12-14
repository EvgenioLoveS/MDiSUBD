import datetime
from db import connect_db
from unauthorized_menu import filter_products, view_catalog  # Импортируем функцию подключения из db_connection.py

# Функция для получения полной информации о клиенте 
def get_user_data(client_id):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT client_id, first_name, last_name, phone, email
            FROM client
            WHERE client_id = %s
        """, (client_id,))
        client_data = cursor.fetchone()
        cursor.close()
        conn.close()

        if client_data:
            print(f"""
            ID клиента: {client_data[0]}
            Имя: {client_data[1]}
            Фамилия: {client_data[2]}
            Телефон: {client_data[3]}
            Email: {client_data[4]}
            """)
        else:
            print("Данные клиента не найдены.")

    else:
        print("Не удалось подключиться к базе данных.")
        return None


# Функция для получения и отображения элементов корзины клиента
def get_cart_items(client_id):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.name, p.brand, ci.product_quantity, ci.product_price, (ci.product_quantity * ci.product_price) AS total_price
            FROM cart_item ci
            JOIN product p ON ci.product_id = p.product_id
            JOIN cart c ON ci.cart_id = c.cart_id
            WHERE c.client_id = %s
        """, (client_id,))
        cart_items = cursor.fetchall()
        cursor.close()
        conn.close()

        # Проверяем, есть ли элементы в корзине
        if cart_items:
            for idx, item in enumerate(cart_items, start=1):
                print(f"""
                Товар {idx}:
                - Название: {item[0]}
                - Бренд: {item[1]}
                - Количество: {item[2]}
                - Цена за единицу: {item[3]:.2f}
                - Общая стоимость: {item[4]:.2f}
                """)
            # Получаем общую стоимость корзины
            total_price = get_cart_total_price(client_id)
            if total_price is not None:
                print(f"Общая стоимость корзины: {total_price:.2f}")
            else:
                print("Не удалось получить общую стоимость корзины.")
        else:
            print("Ваша корзина пуста или не удалось получить данные.")
    else:
        print("Не удалось подключиться к базе данных.")


# Функция для получения общей стоимости корзины клиента
def get_cart_total_price(client_id):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT price
            FROM cart
            WHERE client_id = %s
        """, (client_id,))
        total_price = cursor.fetchone()
        cursor.close()
        conn.close()
        return total_price[0] if total_price else None
    else:
        print("Не удалось подключиться к базе данных.")
        return None


# Функция для добавления товара в корзину
def add_to_cart(client_id):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()

        # Выводим доступные товары
        cursor.execute("""
            SELECT product_id, name, brand, price, quantity
            FROM product
            WHERE quantity > 0
        """)
        products = cursor.fetchall()

        if not products:
            print("Нет доступных товаров для добавления в корзину.")
            cursor.close()
            conn.close()
            return

        print("\nДоступные товары:")
        for product in products:
            print(f"ID: {product[0]}, Название: {product[1]}, Бренд: {product[2]}, Цена: {product[3]:.2f}, Количество на складе: {product[4]}")

        try:
            product_id = int(input("Введите ID товара, который хотите добавить: "))
            product_quantity = int(input("Введите количество: "))

            # Проверяем наличие товара и достаточное количество
            cursor.execute("""
                SELECT quantity, price
                FROM product
                WHERE product_id = %s
            """, (product_id,))
            product_data = cursor.fetchone()

            if not product_data:
                print("Товар с таким ID не найден.")
            elif product_quantity > product_data[0]:
                print("На складе недостаточно товара.")
            else:
                # Получаем ID корзины клиента
                cursor.execute("""
                    SELECT cart_id
                    FROM cart
                    WHERE client_id = %s
                """, (client_id,))
                cart_id = cursor.fetchone()

                if not cart_id:
                    print("У клиента нет корзины.")
                else:
                    cart_id = cart_id[0]
                    product_price = product_data[1]

                    # Добавляем товар в корзину
                    cursor.execute("""
                        INSERT INTO cart_item (cart_id, product_id, product_quantity, product_price)
                        VALUES (%s, %s, %s, %s)
                    """, (cart_id, product_id, product_quantity, product_price))


                    print("Товар успешно добавлен в корзину.")

            conn.commit()
        except ValueError:
            print("Ошибка: некорректный ввод.")
        finally:
            cursor.close()
            conn.close()
    else:
        print("Не удалось подключиться к базе данных.")


def create_order(client_id):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()

        # Получаем общую стоимость корзины
        cursor.execute("""
            SELECT price
            FROM cart
            WHERE client_id = %s
        """, (client_id,))
        total_price = cursor.fetchone()

        if not total_price:
            print("Ваша корзина пуста. Невозможно оформить заказ.")
            cursor.close()
            conn.close()
            return

        total_price = total_price[0]

        # Создаем заказ
        cursor.execute("""
            INSERT INTO "order" (client_id, price)
            VALUES (%s, %s)
            RETURNING order_id
        """, (client_id, total_price))
        order_id = cursor.fetchone()[0]

        conn.commit()
        print(f"Заказ успешно оформлен! Номер заказа: {order_id}, Общая стоимость: {total_price:.2f}")
        cursor.close()
        conn.close()
    else:
        print("Не удалось подключиться к базе данных.")


def view_orders(client_id):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT o.order_id, o.date, o.price
            FROM "order" o
            WHERE o.client_id = %s
            ORDER BY o.date DESC
        """, (client_id,))
        orders = cursor.fetchall()
        cursor.close()
        conn.close()

        if orders:
            print("\n" + "=" * 50)
            print("🛍️ ВАШИ ЗАКАЗЫ".center(50))
            print("=" * 50)

            for order in orders:
                order_id = order[0]
                order_date = order[1].strftime("%d.%m.%Y %H:%M")
                order_price = order[2]

                print(f"\n🆔 Номер заказа: {order_id}")
                print(f"📅 Дата оформления: {order_date}")
                print(f"💰 Общая стоимость: {order_price:.2f} руб.")
                print("-" * 50)
                print("📦 Состав заказа:")
                view_order_items(order_id)
                print("=" * 50)
        else:
            print("У вас нет заказов.")
    else:
        print("Не удалось подключиться к базе данных.")

def view_order_items(order_id):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.name, oi.product_quantity, oi.product_price, 
                   (oi.product_quantity * oi.product_price) AS total_price
            FROM order_item oi
            JOIN product p ON oi.product_id = p.product_id
            WHERE oi.order_id = %s
        """, (order_id,))
        order_items = cursor.fetchall()
        cursor.close()
        conn.close()

        if order_items:
            for idx, item in enumerate(order_items, start=1):
                print(f"""
                {idx}. Название: {item[0]}
                   🔸 Количество: {item[1]}
                   🔸 Цена за единицу: {item[2]:.2f} руб.
                   🔸 Общая стоимость: {item[3]:.2f} руб.
                """)
        else:
            print("❌ Нет товаров в этом заказе.")


def log_action(client_id, action):
    connection = connect_db()
    cursor = connection.cursor()
    try:
        cursor.execute("""
            INSERT INTO logs (client_id, action)
            VALUES (%s, %s)
        """, (client_id, action))
        connection.commit()
        print(f"✅ Лог записан: {action}")
    except Exception as e:
        print(f"❌ Ошибка при записи лога: {e}")
    finally:
        cursor.close()
        connection.close()

# Меню для клиента
def client_menu(user_id):
    while True:
        print("\n" + "=" * 50)
        print("🛒 МЕНЮ КЛИЕНТА".center(50))
        print("=" * 50)
        print("1. Просмотр своих личных данных")
        print("2. Просмотр каталога товаров")
        print("3. Фильтрация товаров")
        print("4. Просмотр корзины")
        print("5. Добавить товар в корзину")
        print("6. Оформить заказ")
        print("7. Просмотр заказов")
        print("8. Вернуться в главное меню")
        print("=" * 50)

        choice = input("Выберите опцию (1, 2, 3, 4, 5, 6, 7, 8): ")

        if choice == '1':
            print("Ваши личные данные:")
            get_user_data(user_id)
            log_action(user_id, "Просмотр личных данных")
        elif choice == '2':  # Обработка опции просмотра каталога
            print("Просмотр каталога товаров...")
            view_catalog()
            log_action(user_id, "Просмотр каталога товаров")
        elif choice == '3':  # Обработка опции фильтрации товаров
            print("Фильтрация товаров...")
            filter_products()
            log_action(user_id, "Фильтрация товаров")
        elif choice == '4':  # Новый пункт меню: просмотр корзины
            print("Элементы вашей корзины:")
            get_cart_items(user_id)
        elif choice == '5':  # Обработка нового пункта
            add_to_cart(user_id)
            log_action(user_id, "Добавление товара в корзину")
        elif choice == '6':  # Оформление заказа
            create_order(user_id)
            log_action(user_id, "Оформление заказа")
        elif choice == '7':  # Просмотр заказов
            print("Просмотр ваших заказов...")
            view_orders(user_id)
            log_action(user_id, "Просмотр заказов")
        elif choice == '8':
            print("Возвращаемся в главное меню.")
            log_action(user_id, "Выход из клиентского меню")
            break
        else:
            print("Неверный выбор. Пожалуйста, выберите опцию 1, 2, 3, 4, 5, 6, 7 или 8.")
