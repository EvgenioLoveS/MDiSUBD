-- Вставка категорий продуктов
INSERT INTO product_category (name) VALUES
('Смартфоны'),
('Ноутбуки'),
('Телевизоры'),
('Наушники'),
('Камеры');

-- Вставка продуктов
INSERT INTO product (product_category_id, price, name, production_date, quantity, brand, description) VALUES
(1, 20000.00, 'Смартфон Galaxy S21', '2021-01-29', 50, 'Samsung', 'Смартфон с 108 МП камерой'),
(2, 80000.00, 'Ноутбук Dell XPS 13', '2021-06-01', 30, 'Dell', 'Ноутбук с процессором Intel i7'),
(3, 50000.00, 'Телевизор LG OLED', '2021-03-15', 20, 'LG', 'Телевизор с поддержкой 4K'),
(4, 3000.00, 'Наушники Sony WH-1000XM4', '2021-02-10', 100, 'Sony', 'Беспроводные наушники с шумоподавлением'),
(5, 25000.00, 'Камера Canon EOS 90D', '2021-05-20', 15, 'Canon', 'Камера с высоким разрешением');

-- Вставка скидок
INSERT INTO discount (description, name, percent, is_active) VALUES
('Летняя распродажа', 'Скидка на смартфоны', 10, TRUE),
('Скидка на ноутбуки', 'Скидка 15% на все ноутбуки', 15, TRUE),
('Скидка на наушники', 'Скидка 20% на наушники', 20, TRUE);

-- Вставка связей между продуктами и скидками
INSERT INTO product_discount (product_id, discount_id) VALUES
(1, 1),  -- Смартфон Galaxy S21 со скидкой 10%
(2, 2),  -- Ноутбук Dell XPS 13 со скидкой 15%
(4, 3);  -- Наушники Sony WH-1000XM4 со скидкой 20%


-- Вставка клиентов с указанием cart_id
INSERT INTO client (first_name, last_name, phone, password, email) VALUES
('Иван', 'Иванов', '+375445905212', 'ivan123', 'ivan@example.com'),
('Петр', 'Петров', '+375445905213', 'petr123', 'petr@example.com'),
('Светлана', 'Сидорова', '+375445905214', 'svetlana123', 'svetlana@example.com');

-- Вставка корзины
INSERT INTO cart (client_id, price) VALUES
(1, 5000.00),
(2, 3000.00),
(3, 2000.00);

-- Вставка товаров в корзину
INSERT INTO cart_item (cart_id, product_id, product_quantity, product_price) VALUES
(1, 1, 1, 20000.00),
(1, 3, 1, 50000.00),
(2, 4, 2, 6000.00);

-- Вставка записей в логи
INSERT INTO logs (client_id, action, timestamp) VALUES
(1, 'Добавлен в корзину продукт: Смартфон Galaxy S21', NOW()),
(2, 'Оформлен заказ: Заказ #1', NOW()),
(3, 'Добавлен в корзину продукт: Наушники Sony WH-1000XM4', NOW()),
(1, 'Оставлен отзыв: Отличный смартфон', NOW());

-- Вставка отзывов
INSERT INTO review (product_id, client_id, content, rating, date) VALUES
(1, 1, 'Отличный смартфон, очень доволен!', 5, NOW()),
(2, 2, 'Хороший ноутбук для работы.', 4, NOW()),
(3, 1, 'Телевизор с отличной картинкой.', 5, NOW()),
(4, 3, 'Наушники просто шикарные!', 5, NOW()),
(5, 1, 'Камера отличного качества, рекомендую!', 4, NOW());

-- Вставка ролей сотрудников
INSERT INTO employee_role (name) VALUES
('Менеджер'),
('Кассир'),
('Администратор');

-- Вставка сотрудников
INSERT INTO employee (employee_role_id, first_name, last_name, salary, phone, position, password, email) VALUES
(1, 'Алексей', 'Смирнов', 50000.00, '+375445905215', 'Менеджер', 'alex123', 'alex@example.com'),
(2, 'Екатерина', 'Федорова', 60000.00, '+375445905216', 'Кассир', 'ekaterina123', 'ekaterina@example.com');


-- Вставка заказов с указанием даты и исправленными ценами
INSERT INTO "order" (client_id, date, price) VALUES
(1, '2024-10-10 10:00:00', 23000.00),  -- Заказ клиента Иванов на сумму 23000
(2, '2024-10-11 12:30:00', 80000.00),  -- Заказ клиента Петров на сумму 80000
(3, '2024-10-11 14:15:00', 75000.00);  -- Заказ клиента Сидорова на сумму 75000

-- Вставка элементов заказа
INSERT INTO "order_item" (order_id, product_id, product_quantity, product_price) VALUES
(1, 1, 1, 20000.00),  -- Заказ #1: Смартфон Galaxy S21
(1, 4, 1, 3000.00),   -- Заказ #1: Наушники Sony WH-1000XM4
(2, 2, 1, 80000.00),  -- Заказ #2: Ноутбук Dell XPS 13
(3, 3, 1, 50000.00),  -- Заказ #3: Телевизор LG OLED
(3, 5, 1, 25000.00);  -- Заказ #3: Камера Canon EOS 90D
