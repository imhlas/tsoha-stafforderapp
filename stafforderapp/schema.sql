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
    product_number INTEGER 
);

CREATE TABLE images (
    id SERIAL PRIMARY KEY,
    product_number INTEGER,
    data BYTEA
);
