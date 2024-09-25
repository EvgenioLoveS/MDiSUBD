# Internet-Shop Electronics

>Тема: Интернет-магазин электроники  
>Группа: 253504  
>Автор: Жгутов Евгений Дмитриевич

- [Функциональные требования](#функциональные-требования) ()
- [Перечень сущностей](#сущности)

### Функциональные требования:
1. Авторизация пользователя.
2. Управление пользователями (CRUD).
3. Система ролей.
4. Журналирование действий пользователя.
5. Типы пользователей и их возможности:
    - **Неавторизованный клиент**:
        + Может просматривать каталог товаров.
        + Может фильтровать товары по различным параметрам.
    - **Авторизованный клиент** (то же, что и неавторизованный, а также):
        + Добавлять товары в корзину.
        + Оформлять заказ.
    - **Сотрудник**:
        + Управлять товарами и категориями (CRUD).
        + Управлять скидками (CRUD).
        + Просматривать информацию о пользователях и заказах.
---
### Сущности:
1. **Товар**:
    - Таблица: **product**.
    - Поля:
        + price DECIMAL 
        + name VARCHAR 
        + production_date DATE 
        + quantity INT 
        + brand VARCHAR 
        + description VARCHAR
    - Связи:
        + один ко многим с _order_item_
        + один ко многим с _review_
        + один ко многим с _cart_item_
        + многие к одному с _product_category_
        + многие ко многим с _discount_
2. **Категория товара**:
    - Таблица: **product_category**.
    - Поля:
        + name VARCHAR
    - Связи:
        + один ко многим с _product_
3. **Сотрудник**:
    - Таблица: **employee**.
    - Поля:
        + first_name VARCHAR 
        + last_name VARCHAR 
        + salary DECIMAL  
        + phone CHAR
        + position VARCHAR 
        + password VARCHAR 
        + email VARCHAR 
    - Связи:
        + многик к одному с _employee_role_
4. **Роль сотрудника**:
    - Таблица: **employee_role**.
    - Поля:
        + name VARCHAR
    - Связи:
        + один ко многим с _employee_
5. **Клиент**:
    - Таблица: **client**.
    - Поля:
        + name VARCHAR
        + phone CHAR 
        + password VARCHAR 
        + email VARCHAR 
    - Связи:
        + один ко многим с _review_
        + один к одному с _cart_
        + один ко многим с _order_
6. **Заказ**:
    - Таблица: **order**.
    - Поля:
        + date DATETIME 
        + price DECIMAL  
    - Связи:
        + многие к одному с _client_
        + один ко многим с _order_item_
7. **Элемент заказа**:
    - Таблица: **order_item**.
    - Поля:
        + product_quantity INT 
        + product_price DECIMAL  
    - Связи:
        + многие к одному с _order_
        + многие к одному с _product_
8. **Корзина**:
    - Таблица: **cart**.
    - Поля:
        + price DECIMAL 
    - Связи:
        + один к одному с _client_
        + один ко многим с _cart_item_
9. **Элемент корзины**:
    - Таблица: **cart_item**.
    - Поля:
        + product_quantity INT 
        + product_price DECIMAL 
    - Связи:
        + многие к одному с _cart_
        + многие к одному с _product_
10. **Отзыв**:
    - Таблица: **review**.
    - Поля:
        + content VARCHAR 
        + rating INT 
        + date DATETIME 
    - Связи:
        + многие к одному с _client_
        + многие к одному с _product_
11. **Акция**:
    - Таблица: **discount**.
    - Поля:
        + description VARCHAR 
        + name VARCHAR 
        + percent INT 
        + is_active BOLLEAN 
    - Связи:
        + многие ко многим с _product_
12. **Журнал действий**:
    - Таблица: **logs**.
    - Поля:
        + id INT 
        + user_id INT 
        + action VARCHAR 
        + timestamp DATETIME 
    - Связи:
        + один ко многим с _client_
