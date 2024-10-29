DROP TABLE IF EXISTS "product_discount" CASCADE;
DROP TABLE IF EXISTS "cart_item" CASCADE;
DROP TABLE IF EXISTS "cart" CASCADE;
DROP TABLE IF EXISTS "employee" CASCADE;
DROP TABLE IF EXISTS "employee_role" CASCADE;
DROP TABLE IF EXISTS "order_item" CASCADE;
DROP TABLE IF EXISTS "order" CASCADE;
DROP TABLE IF EXISTS "review" CASCADE;
DROP TABLE IF EXISTS "discount" CASCADE;
DROP TABLE IF EXISTS "logs" CASCADE;
DROP TABLE IF EXISTS "client" CASCADE;
DROP TABLE IF EXISTS "product" CASCADE;
DROP TABLE IF EXISTS "product_category" CASCADE;
  

CREATE TABLE "product" (
    "product_id" serial PRIMARY KEY,
    "product_category_id" int NOT NULL,
    "price" numeric(7, 2) NOT NULL CONSTRAINT positive_price CHECK(price > 0),
    "name" varchar(30) NOT NULL,
    "production_date" date NOT NULL,
    "quantity" int NOT NULL CONSTRAINT non_negative_quantity CHECK(quantity >= 0),
    "brand" varchar(30) NOT NULL,
    "description" text NOT NULL
);

CREATE TABLE "product_category" (
    "product_category_id" serial PRIMARY KEY,
    "name" varchar(30) NOT NULL
);

CREATE TABLE "client" (
    "client_id" serial PRIMARY KEY,
    "first_name" varchar(30) NOT NULL,
    "last_name" varchar(30) NOT NULL,
    "phone" char(13) NOT NULL,
    "password" varchar(20) NOT NULL,
    "email" varchar(30) UNIQUE NOT NULL
);

CREATE TABLE "logs" (
    "id" serial PRIMARY KEY,
    "client_id" int NOT NULL,  -- FK на таблицу client
    "action" varchar(255) NOT NULL,
    "timestamp" timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE "employee" (
    "employee_id" serial PRIMARY KEY,
    "employee_role_id" int NOT NULL,
    "first_name" varchar(30) NOT NULL,
    "last_name" varchar(30) NOT NULL,
    "salary" numeric(7, 2) NOT NULL CONSTRAINT positive_salary CHECK(salary > 0),
    "phone" char(13) NOT NULL,
    "position" varchar(30) NOT NULL,
    "password" varchar(20) NOT NULL,
    "email" varchar(30) NOT NULL
);

CREATE TABLE "employee_role" (
    "employee_role_id" serial PRIMARY KEY,
    "name" varchar(30) NOT NULL
);

CREATE TABLE "order" (
    "order_id" serial PRIMARY KEY,
    "client_id" int NOT NULL,
    "date" timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "price" numeric(7, 2) NOT NULL CONSTRAINT positive_price CHECK(price > 0)
);

CREATE TABLE "order_item" (
    "order_item_id" serial PRIMARY KEY,
    "order_id" int NOT NULL,
    "product_id" int NOT NULL,
    "product_quantity" int NOT NULL CONSTRAINT positive_product_quantity CHECK(product_quantity > 0),
    "product_price" numeric(7, 2) NOT NULL CONSTRAINT positive_product_price CHECK(product_price > 0)
);

CREATE TABLE "cart" (
    "cart_id" serial PRIMARY KEY,
    "client_id" int UNIQUE NOT NULL,
    "price" numeric(7, 2) NOT NULL CONSTRAINT non_negative_price CHECK(price >= 0)
);

CREATE TABLE "cart_item" (
    "cart_item_id" serial PRIMARY KEY,
    "cart_id" int NOT NULL,
    "product_id" int NOT NULL,
    "product_quantity" int NOT NULL CONSTRAINT positive_product_quantity CHECK(product_quantity > 0),
    "product_price" numeric(7, 2) NOT NULL CONSTRAINT positive_product_price CHECK(product_price > 0)
);

CREATE TABLE "review" (
    "review_id" serial PRIMARY KEY,
    "product_id" int NOT NULL,
    "client_id" int NOT NULL,
    "content" text NOT NULL,
    "rating" int NOT NULL CONSTRAINT one_to_five_rating_range CHECK(
        rating > 0
        AND rating < 6
    ),
    "date" timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE "discount" (
    "discount_id" serial PRIMARY KEY,
    "description" varchar(50) NOT NULL,
    "name" varchar(30) NOT NULL,
    "percent" int NOT NULL CONSTRAINT discount_percent_value CHECK(
        percent > 0
        AND percent < 100
    ),
    "is_active" boolean NOT NULL
);

CREATE TABLE "product_discount" (
    "product_id" int NOT NULL,
    "discount_id" int NOT NULL,
    PRIMARY KEY ("product_id", "discount_id")
);

-- Добавляем внешние ключи

ALTER TABLE "product"
ADD FOREIGN KEY ("product_category_id") REFERENCES "product_category" ("product_category_id") ON DELETE RESTRICT;

ALTER TABLE "order"
ADD FOREIGN KEY ("client_id") REFERENCES "client" ("client_id") ON DELETE CASCADE;

ALTER TABLE "review"
ADD FOREIGN KEY ("client_id") REFERENCES "client" ("client_id") ON DELETE CASCADE;

ALTER TABLE "review"
ADD FOREIGN KEY ("product_id") REFERENCES "product" ("product_id") ON DELETE CASCADE;

ALTER TABLE "order_item"
ADD FOREIGN KEY ("order_id") REFERENCES "order" ("order_id") ON DELETE CASCADE;

ALTER TABLE "order_item"
ADD FOREIGN KEY ("product_id") REFERENCES "product" ("product_id") ON DELETE RESTRICT;

ALTER TABLE "employee"
ADD FOREIGN KEY ("employee_role_id") REFERENCES "employee_role" ("employee_role_id") ON DELETE RESTRICT;

ALTER TABLE "cart"
ADD FOREIGN KEY ("client_id") REFERENCES "client" ("client_id") ON DELETE CASCADE;

ALTER TABLE "cart_item"
ADD FOREIGN KEY ("cart_id") REFERENCES "cart" ("cart_id") ON DELETE CASCADE;

ALTER TABLE "cart_item"
ADD FOREIGN KEY ("product_id") REFERENCES "product" ("product_id") ON DELETE RESTRICT;

ALTER TABLE "product_discount"
ADD FOREIGN KEY ("product_id") REFERENCES "product" ("product_id") ON DELETE CASCADE;

ALTER TABLE "product_discount"
ADD FOREIGN KEY ("discount_id") REFERENCES "discount" ("discount_id") ON DELETE CASCADE;

ALTER TABLE "logs"
ADD FOREIGN KEY ("client_id") REFERENCES "client" ("client_id") ON DELETE CASCADE;  -- Внешний ключ для таблицы logs

-- Создаем индексы для улучшения производительности

-- PRODUCT 
CREATE INDEX idx_product_product_category_id ON product ("product_category_id");
CREATE INDEX idx_product_name ON product ("name");
CREATE INDEX idx_product_brand ON product ("brand");

-- PRODUCT_CATEGORY 
CREATE INDEX idx_product_category_name ON product_category ("name");

-- CLIENT 
CREATE INDEX idx_client_email ON client ("email");

-- EMPLOYEE 
CREATE INDEX idx_employee_email ON employee ("email");
CREATE INDEX idx_employee_employee_role_id ON employee("employee_role_id");

-- ORDER
CREATE INDEX idx_order_date ON "order" ("date");
CREATE INDEX idx_order_client_id ON "order" ("client_id");

-- ORDER_ITEM
CREATE INDEX idx_order_item_order_id ON order_item ("order_id");
CREATE INDEX idx_order_item_product_id ON order_item ("product_id");

-- CART
CREATE INDEX idx_cart_client_id ON cart ("client_id");

-- CART_ITEM
CREATE INDEX idx_cart_item_cart_id ON cart_item ("cart_id");
CREATE INDEX idx_cart_item_product_id ON cart_item ("product_id");

-- REVIEW
CREATE INDEX idx_review_product_id ON review ("product_id");
CREATE INDEX idx_review_client_id ON review ("client_id");

-- DISCOUNT
CREATE INDEX idx_discount_percent ON discount ("percent");
CREATE INDEX idx_product_discount_product_id ON product_discount ("product_id");
CREATE INDEX idx_product_discount_discount_id ON product_discount ("discount_id");

-- LOGS
CREATE INDEX idx_logs_client_id ON logs ("client_id");
CREATE INDEX idx_logs_timestamp ON logs ("timestamp");

