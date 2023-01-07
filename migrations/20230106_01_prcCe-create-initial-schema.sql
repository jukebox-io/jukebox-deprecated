-- Create initial schema
-- depends:

DROP TABLE IF EXISTS app_user;

CREATE TABLE IF NOT EXISTS app_user (
    username varchar(45) NOT NULL,
    password varchar(450) NOT NULL,
    enabled integer NOT NULL DEFAULT '1',
    PRIMARY KEY (username)
)