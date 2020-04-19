DO $$
BEGIN
  CREATE ROLE m4m LOGIN
  ENCRYPTED PASSWORD 'md52b9f351ef8b847d8506328e34717eeea'
  NOSUPERUSER INHERIT CREATEDB NOCREATEROLE NOREPLICATION;
  EXCEPTION WHEN DUPLICATE_OBJECT THEN
  RAISE NOTICE 'User m4m already exists';
END
$$;

CREATE DATABASE m4m
    WITH
    OWNER = m4m
    ENCODING = 'UTF8'
    LC_COLLATE = 'Russian_Russia.1251'
    LC_CTYPE = 'Russian_Russia.1251'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;

CREATE TABLE IF NOT EXISTS objects
(
    id   SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL
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
    id                SERIAL PRIMARY KEY,
    name              VARCHAR NOT NULL,
    controller_id     INT REFERENCES controllers (id),
    activation_date   DATE DEFAULT NULL,
    status            INT  DEFAULT NULL,
    deactivation_date DATE DEFAULT NULL,
    sensor_type       INT  DEFAULT NULL
);
ALTER TABLE sensors OWNER TO m4m;

CREATE TABLE IF NOT EXISTS sensor_data
(
    id                SERIAL PRIMARY KEY,
    sensor_id         INTEGER REFERENCES sensors(id),
    data              JSON NOT NULL
);
ALTER TABLE sensor_data OWNER TO m4m;

CREATE TABLE IF NOT EXISTS users
(
  id SERIAL PRIMARY KEY,
  username VARCHAR NOT NULL UNIQUE,
  pwd_hash VARCHAR NOT NULL
);
ALTER TABLE users OWNER TO m4m;

INSERT INTO objects VALUES (
  1,
  'Mercedes'
);

INSERT INTO controllers VALUES (
  1,
  'OBD',
  1,
  NULL,
  NULL,
  NULL,
  5
);

INSERT INTO sensors VALUES (
  6,
  'OBD',
  1,
  NULL,
  NULL,
  NULL,
  5
);

INSERT INTO sensors VALUES (
  7,
  'GPS',
  1,
  NULL,
  NULL,
  NULL,
  6
);

INSERT INTO sensor_data VALUES (
  default,
  6,
  '{"timestamp":"", "value": {}}'
);

INSERT INTO sensor_data VALUES (
  default,
  7,
  '{"timestamp":"", "value": {}}'
);
