-- Выборка всех продуктов
SELECT * FROM product;
-- Выборка всех категорий продуктов
SELECT * FROM product_category;
-- Выборка всех клиентов
SELECT * FROM client;
-- Выборка всех заказов
SELECT * FROM "order";
-- Выборка всех товаров в заказе
SELECT * FROM order_item;
-- Выборка всех сотрудников
SELECT * FROM employee;
-- Выборка всех отзывов
SELECT * FROM review;
-- Выборка всех корзин
SELECT * FROM cart;
-- Выборка всех товаров в корзине
SELECT * FROM cart_item;
-- Выборка всех скидок
SELECT * FROM discount;
-- Выборка всех скидок на продукты
SELECT * FROM product_discount;
-- Выборка всех логов действий клиентов
SELECT * FROM logs;
--Выборка всех клиентов с их заказами
SELECT client.client_id, client.first_name, client.last_name, "order".order_id, "order".date
FROM client
JOIN "order" ON client.client_id = "order".client_id;
--Выборка всех продуктов с их категориями
SELECT product.product_id, product.name, product_category.name AS category_name
FROM product
JOIN product_category ON product.product_category_id = product_category.product_category_id;
--Выборка всех заказов с их товарами
SELECT "order".order_id, product.name, order_item.product_quantity
FROM "order"
JOIN order_item ON "order".order_id = order_item.order_id
JOIN product ON order_item.product_id = product.product_id;
--Выборка всех отзывов с привязкой к продуктам
SELECT review.review_id, product.name, review.content
FROM review
JOIN product ON review.product_id = product.product_id;
--Выборка всех продуктов, участвующих в скидках
SELECT product.name, discount.percent
FROM product
JOIN product_discount ON product.product_id = product_discount.product_id
JOIN discount ON product_discount.discount_id = discount.discount_id;
--Выборка всех клиентов с количеством их заказов
SELECT client.client_id, client.first_name, client.last_name, COUNT("order".order_id) AS total_orders
FROM client
JOIN "order" ON client.client_id = "order".client_id
GROUP BY client.client_id;
--Выборка всех товаров в корзинах клиентов
SELECT cart.cart_id, product.name, cart_item.product_quantity
FROM cart
JOIN cart_item ON cart.cart_id = cart_item.cart_id
JOIN product ON cart_item.product_id = product.product_id;
--Выборка самых продаваемых товаров
SELECT product.name, SUM(order_item.product_quantity) AS total_sold
FROM product
JOIN order_item ON product.product_id = order_item.product_id
GROUP BY product.name
ORDER BY total_sold DESC;
--Выборка активных скидок на текущий момент
SELECT discount.discount_id, discount.name, discount.percent, discount.is_active
FROM discount
WHERE discount.is_active = TRUE;
--Выборка клиентов у которых моб. телефон заканчивается на 1 
SELECT * FROM client
WHERE phone LIKE '%1';
--Запрос для сортировки клиентов по email
SELECT client_id, first_name, last_name, email 
FROM client 
ORDER BY email ASC;
--Уникальные телефонные номера клиентов
SELECT DISTINCT phone 
FROM client;
--обновление данных клиента
UPDATE client
SET phone = '+1234567890'
WHERE client_id = 1;
--Удаление клиента по его идентификатору
DELETE FROM client
WHERE client_id = 2;
--Вставка нового клиента с полными данными
INSERT INTO client (first_name, last_name, phone, password, email)
VALUES ('Иван', 'Иванов', '+79991234567', 'password123', 'ivanov@example.com');
