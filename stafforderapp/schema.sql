CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT,
    password TEXT,
    role INTEGER
);

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name TEXT,
    price DECIMAL(10, 2),
    product_number INTEGER,
    brand_id INTEGER
);

CREATE TABLE images (
    id SERIAL PRIMARY KEY,
    product_number INTEGER,
    data BYTEA
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    order_date DATE,
    order_status TEXT
);

CREATE TABLE order_details (
    id SERIAL PRIMARY KEY,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    price DECIMAL(10,2)
);

CREATE TABLE brands (
    id SERIAL PRIMARY KEY,
    name TEXT,
    logo BYTEA
);
