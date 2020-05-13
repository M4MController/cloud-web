CREATE TABLE IF NOT EXISTS users
(
  id SERIAL PRIMARY KEY,
  login VARCHAR NOT NULL UNIQUE,
  pwd_hash VARCHAR NOT NULL
);
ALTER TABLE users OWNER TO m4m;

CREATE TABLE IF NOT EXISTS users_info
(
  user_id INTEGER PRIMARY KEY REFERENCES users(id),
  family_name VARCHAR,
  username VARCHAR,
  second_name VARCHAR,
  date_receiving INTEGER,
  issued_by VARCHAR,
  division_number VARCHAR,
  registration_addres VARCHAR,
  mailing_addres VARCHAR,
  birth_day VARCHAR,
  sex BOOLEAN,
  home_phone VARCHAR,
  mobile_phone VARCHAR,
  citizenship VARCHAR,
  e_mail VARCHAR
);
ALTER TABLE users_info OWNER TO m4m;

CREATE TABLE IF NOT EXISTS companies
(
  id INTEGER PRIMARY KEY,
  name VARCHAR,
);
ALTER TABLE comanies OWNER TO m4m;

CREATE TABLE IF NOT EXISTS objects
(
    id   SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    user_id INTEGER REFERENCES users(id)
);
ALTER TABLE objects OWNER TO m4m;

CREATE TABLE IF NOT EXISTS controllers
(
    id                SERIAL PRIMARY KEY,
    name              VARCHAR,
    object_id         INT REFERENCES objects (id),
    meta              TEXT,
    activation_date   DATE DEFAULT NULL,
    status            INT  DEFAULT NULL,
    mac               VARCHAR NOT NULL UNIQUE,
    deactivation_date DATE DEFAULT NULL,
    controller_type   INT  DEFAULT NULL
);
ALTER TABLE controllers OWNER TO m4m;

CREATE TABLE IF NOT EXISTS sensors
(
    id                CHAR(32) UNIQUE NOT NULL PRIMARY KEY,
    name              VARCHAR NOT NULL,
    controller_id     INT REFERENCES controllers (id),
    activation_date   DATE DEFAULT NULL,
    status            INT  DEFAULT NULL,
    deactivation_date DATE DEFAULT NULL,
    sensor_type       INT  DEFAULT NULL,
    company_id        INT REFERENCES companies (id),
);
ALTER TABLE sensors OWNER TO m4m;

CREATE TABLE IF NOT EXISTS users_social_tokens (
  user_id INTEGER PRIMARY KEY REFERENCES users(id),
  yandex_disk VARCHAR
);
