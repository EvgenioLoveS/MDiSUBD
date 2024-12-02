SELECT *
from cart;

INSERT INTO client (first_name, last_name, phone, password, email)
VALUES ('Константин', 'Петров', '+375445905218', 'konstantin111', 'konstantin@gmail.com');

SELECT *
from cart;

-- Добавляем продукт (Наушники Sony WH-1000XM4) в корзину клиента Петров (cart_id = 5)
INSERT INTO cart_item (cart_id, product_id, product_quantity, product_price)
VALUES (5, 4, 3, 3000.00);

select *
from cart;


