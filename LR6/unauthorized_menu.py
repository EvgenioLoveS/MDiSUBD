from db import connect_db  # Импортируем функцию подключения из db_connection.py

# Функция для получения всех товаров из базы данных
def get_all_products():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.product_id, p.name, p.price, p.brand, c.name AS category
            FROM product p
            JOIN product_category c ON p.product_category_id = c.product_category_id
        """)
        products = cursor.fetchall()
        cursor.close()
        conn.close()
        return products
    else:
        print("Не удалось подключиться к базе данных.")
        return []

# Функция для получения фильтрованных товаров по цене
def filter_products_by_price(min_price, max_price):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.product_id, p.name, p.price, p.brand, c.name AS category
            FROM product p
            JOIN product_category c ON p.product_category_id = c.product_category_id
            WHERE p.price BETWEEN %s AND %s
        """, (min_price, max_price))
        products = cursor.fetchall()
        cursor.close()
        conn.close()
        return products
    else:
        print("Не удалось подключиться к базе данных.")
        return []

# Функция для фильтрации товаров по категории
def filter_products_by_category(category):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.product_id, p.name, p.price, p.brand, c.name AS category
            FROM product p
            JOIN product_category c ON p.product_category_id = c.product_category_id
            WHERE c.name = %s
        """, (category,))
        products = cursor.fetchall()
        cursor.close()
        conn.close()
        return products
    else:
        print("Не удалось подключиться к базе данных.")
        return []

# Функция для фильтрации товаров по рейтингу
def filter_products_by_rating(min_rating):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.product_id, p.name, p.price, p.brand, c.name AS category
            FROM product p
            JOIN product_category c ON p.product_category_id = c.product_category_id
            WHERE EXISTS (
                SELECT 1 FROM review r
                WHERE r.product_id = p.product_id
                AND r.rating >= %s
            )
        """, (min_rating,))
        products = cursor.fetchall()
        cursor.close()
        conn.close()
        return products
    else:
        print("Не удалось подключиться к базе данных.")
        return []

# Функция для отображения каталога товаров
def view_catalog():
    print("\n" + "=" * 50)
    print("                 📦 Каталог товаров")
    print("=" * 50)
    products = get_all_products()
    if products:
        for product in products:
            print(f"🆔 ID: {product[0]} | 📜 Название: {product[1]}")
            print(f"💵 Цена: {product[2]}$ | 🏷️ Бренд: {product[3]} | 🗂️ Категория: {product[4]}")
            print("-" * 50)
    else:
        print("❌ В каталоге товаров ничего не найдено.")
    print("=" * 50)

# Функция для фильтрации товаров
def filter_products():
    print("\n" + "=" * 50)
    print("               🔎 Фильтрация товаров")
    print("=" * 50)
    print("1. По цене")
    print("2. По категории")
    print("3. По рейтингу")
    print("4. Вернуться в меню")
    print("=" * 50)

    choice = input("Выберите опцию (1-4): ")

    if choice == '1':
        print("\n💵 Фильтрация по цене:")
        min_price = float(input("Введите минимальную цену: "))
        max_price = float(input("Введите максимальную цену: "))
        print(f"\n🔍 Товары с ценой от {min_price} до {max_price}:")
        products = filter_products_by_price(min_price, max_price)
        if products:
            for product in products:
                print(f"🆔 ID: {product[0]} | 📜 Название: {product[1]} - {product[2]}$")
                print(f"🏷️ Бренд: {product[3]} | 🗂️ Категория: {product[4]}")
                print("-" * 50)
        else:
            print("❌ Товары не найдены.")
    elif choice == '2':
        print("\n🗂️ Фильтрация по категории:")
        category = input("Введите категорию товара: ")
        print(f"\n🔍 Товары в категории '{category}':")
        products = filter_products_by_category(category)
        if products:
            for product in products:
                print(f"🆔 ID: {product[0]} | 📜 Название: {product[1]} - {product[2]}$")
                print(f"🏷️ Бренд: {product[3]} | 🗂️ Категория: {product[4]}")
                print("-" * 50)
        else:
            print("❌ Товары не найдены.")
    elif choice == '3':
        print("\n⭐ Фильтрация по рейтингу:")
        min_rating = int(input("Введите минимальный рейтинг: "))
        print(f"\n🔍 Товары с рейтингом от {min_rating} и выше:")
        products = filter_products_by_rating(min_rating)
        if products:
            for product in products:
                print(f"🆔 ID: {product[0]} | 📜 Название: {product[1]} - {product[2]}$")
                print(f"🏷️ Бренд: {product[3]} | 🗂️ Категория: {product[4]}")
                print("-" * 50)
        else:
            print("❌ Товары не найдены.")
    elif choice == '4':
        print("↩ Возвращаемся в меню.")
    else:
        print("❌ Неверный выбор. Пожалуйста, выберите опцию от 1 до 4.")

# Функция для отображения меню для неавторизованного клиента
def unauthorized_menu():
    while True:
        print("\n" + "=" * 50)
        print("         🛒 Меню неавторизованного клиента")
        print("=" * 50)
        print("1. Просмотреть каталог товаров")
        print("2. Фильтровать товары")
        print("3. Вернуться в главное меню")
        print("=" * 50)
        
        choice = input("Выберите опцию (1-3): ")

        if choice == '1':
            print("\n🔍 Просмотр каталога товаров...")
            view_catalog()
        elif choice == '2':
            print("\n🔍 Фильтрация товаров...")
            filter_products()
        elif choice == '3':
            print("↩ Возвращаемся в главное меню.")
            break  # Прерываем цикл, чтобы выйти в главное меню
        else:
            print("❌ Неверный выбор. Пожалуйста, выберите опцию от 1 до 3.")

