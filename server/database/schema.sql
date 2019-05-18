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
