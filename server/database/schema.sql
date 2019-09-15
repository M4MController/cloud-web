CREATE TABLE objects
(
    id   SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL
);

CREATE TABLE controllers
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

CREATE TABLE sensors
(
    id                SERIAL PRIMARY KEY,
    name              VARCHAR NOT NULL,
    controller_id     INT REFERENCES controllers (id),
    activation_date   DATE DEFAULT NULL,
    status            INT  DEFAULT NULL,
    deactivation_date DATE DEFAULT NULL,
    sensor_type       INT  DEFAULT NULL
);

CREATE TABLE sensor_data
(
    id                SERIAL PRIMARY KEY,
    sensor_id         INTEGER REFERENCES sensors(id),
    data              JSON NOT NULL,
    sign              BYTEA DEFAULT NULL
);

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
