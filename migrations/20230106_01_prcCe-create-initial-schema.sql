-- Create initial schema
-- depends:

DROP TABLE IF EXISTS app_user;

CREATE TABLE IF NOT EXISTS app_user (
    username varchar(45) NOT NULL,
    password varchar(450) NOT NULL,
    enabled integer NOT NULL DEFAULT '1',
    PRIMARY KEY (username)
);

INSERT INTO app_user VALUES ('user1', 'pass123');
INSERT INTO app_user VALUES ('user2', 'shssjnn');
INSERT INTO app_user VALUES ('user3', 'zmzzjzm');

SELECT * FROM app_user;
