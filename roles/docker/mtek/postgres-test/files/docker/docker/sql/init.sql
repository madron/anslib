CREATE USER test WITH ENCRYPTED PASSWORD 'test' ;
CREATE DATABASE test WITH OWNER test;
\c test;
SET ROLE test;


CREATE TABLE log (
    id              SERIAL,
    insert_time     timestamp   not null default CURRENT_TIMESTAMP,
    data            text        default repeat('1234567890ABCDEF', 64)
);


CREATE TABLE bytea (
    id              SERIAL,
    insert_time     timestamp   not null default CURRENT_TIMESTAMP,
    bytea           bytea
);
