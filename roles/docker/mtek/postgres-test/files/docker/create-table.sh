#!/bin/bash

psql -h postgres -U postgres -c "CREATE DATABASE test;"
psql -h postgres -U postgres -c "CREATE TABLE log (id SERIAL, insert_time timestamp not null default CURRENT_TIMESTAMP);" test
