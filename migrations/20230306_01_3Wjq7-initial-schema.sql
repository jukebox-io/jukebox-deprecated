-- Initial Schema
-- depends: 

DROP TABLE IF EXISTS customer;

CREATE TABLE customer (
    id SERIAL PRIMARY KEY,
    display_name VARCHAR(128) NOT NULL
);
