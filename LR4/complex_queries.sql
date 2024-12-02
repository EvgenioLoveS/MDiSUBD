-- @block
-- Выборка пользователей, которые оставили отзыв с рейтингом >= 3 и начиная с '2023-10-01'
SELECT first_name || ' ' || last_name AS Name,
    email,
    name,
    content,
    rating
FROM client
    JOIN review USING(client_id)
    JOIN product USING(product_id)
WHERE rating >= 3
    AND "date" >= '2023-10-01';

-- @block
-- Выбрать товары категории "Смартфоны", цена которых отличается от минимальной цены в данной категории не более чем на 50 рублей
SELECT p.name,
    price,
    brand,
    description
FROM product p
    JOIN product_category pc ON p.product_category_id = pc.product_category_id
    AND pc.name = 'Смартфоны'
    JOIN (
        SELECT min(price) min_price
        FROM product
            JOIN product_category USING(product_category_id)
        WHERE product_category.name = 'Смартфоны'
    ) AS mp ON p.price - mp.min_price <= 50;

-- @block 
-- выборка продуктов, категории продукта и скидки если есть активные
CREATE VIEW products_active_discounts AS
SELECT pc.name AS Category,
    p.name AS Name,
    price,
    production_date,
    quantity,
    brand,
    p.description,
    d.name AS Discount,
    d.description AS Profit,
    d.percent
FROM product p
    JOIN product_category pc USING(product_category_id)
    LEFT JOIN product_discount USING(product_id)
    LEFT JOIN discount d ON d.discount_id = product_discount.discount_id
    AND d.is_active = TRUE;

SELECT *
FROM products_active_discounts;

-- @block
-- получить клиентов и написанные ими отзывы на конкретные продукты, также продукты на которые не написали отзывов
CREATE VIEW clients_reviews_all_poducts AS
SELECT first_name || ' ' || last_name AS Name,
    email,
    content,
    rating,
    "date",
    p.name AS product,
    CASE
        WHEN r."date" < NOW() - INTERVAL '1 year' THEN 'Очень старый'
        WHEN r."date" < NOW() - INTERVAL '6 months' THEN 'Старый'
        ELSE 'Новый'
    END AS review_age
FROM client
    JOIN review r USING(client_id)
    JOIN product p USING(product_id);

SELECT *
FROM clients_reviews_all_poducts;

-- @block
-- получить заказы для каждого клиента
CREATE VIEW clients_orders AS
SELECT first_name || ' ' || last_name AS "Client name",
    email,
    o."date" AS "Order date",
    o.price AS Total,
    p.name,
    oi.product_quantity
FROM client c
    JOIN "order" o USING(client_id)
    JOIN order_item oi USING(order_id)
    JOIN product p USING(product_id);

SELECT *
FROM clients_orders;

-- @block
-- получить всех людей, которые как либо связаны с магазином
CREATE VIEW all_people AS
SELECT first_name || ' ' || last_name AS Name,
    email
FROM client
UNION
SELECT first_name || ' ' || last_name AS Name,
    email
FROM employee
ORDER BY Name;

SELECT *
FROM all_people;

-- @block
-- получить имена клиентов, которые оформили >= 2 заказов, количество их заказов и общую стоимость
CREATE VIEW clients_more_than_n_orders AS
SELECT first_name || ' ' || last_name AS Name,
    email,
    COUNT(*) AS "Number of orders",
    SUM(o.price) AS Total
FROM client
    JOIN "order" o USING(client_id)
GROUP BY email,
    Name
HAVING COUNT(*) >= 2;

SELECT *
FROM clients_more_than_n_orders;

-- @block
-- получить сотрудников, добавив столбец максимальной ЗП для его должности
CREATE VIEW employees_max_salary AS
SELECT first_name || ' ' || last_name AS Name,
    salary,
    MAX(salary) over(PARTITION by position) AS max_salary,
    DENSE_RANK() over(PARTITION by position) "rank"
FROM employee;

SELECT *
FROM employees_max_salary;