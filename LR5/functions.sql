-- @block
DROP FUNCTION IF EXISTS update_cart_price;

DROP FUNCTION IF EXISTS create_cart_for_new_client;

DROP FUNCTION IF EXISTS copy_cart_items_to_order_items;

-- @block
CREATE OR REPLACE FUNCTION update_cart_price() RETURNS TRIGGER AS $$ BEGIN IF TG_OP = 'DELETE' THEN
UPDATE cart
SET price = price - OLD.product_price * OLD.product_quantity
WHERE cart_id = OLD.cart_id;

ELSIF TG_OP = 'INSERT' THEN
UPDATE cart
SET price = price + NEW.product_price * NEW.product_quantity
WHERE cart_id = NEW.cart_id;

END IF;

RETURN NULL;

END;

$$ LANGUAGE plpgsql;

-----------------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION create_cart_for_new_client() RETURNS TRIGGER AS $$ BEGIN
INSERT INTO cart (client_id, price)
VALUES (NEW.client_id, 0.0);

RETURN NULL;

END;

$$ LANGUAGE plpgsql;

-----------------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION copy_cart_items_to_order_items() RETURNS TRIGGER AS $$
DECLARE cur_cart_id INT;

BEGIN
SELECT cart_id INTO cur_cart_id
FROM cart
WHERE client_id = NEW.client_id;

INSERT INTO order_item (
    order_id,
    product_id,
    product_quantity,
    product_price
  )
SELECT NEW.order_id,
  product_id,
  product_quantity,
  product_price
FROM cart_item
WHERE cart_id = cur_cart_id;

DELETE FROM cart_item
WHERE cart_id = cur_cart_id;

UPDATE cart
SET price = 0
WHERE client_id = NEW.client_id;

RETURN NULL;

END;

$$ LANGUAGE plpgsql;