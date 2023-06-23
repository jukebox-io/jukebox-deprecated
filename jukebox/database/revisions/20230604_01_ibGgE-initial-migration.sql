-- Initial Migration
-- depends: 

DROP TABLE IF EXISTS account;

CREATE TABLE account (
    pid SERIAL PRIMARY KEY
);
