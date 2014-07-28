#!/bin/bash

while true
do
    psql -h postgres -U postgres -c "INSERT INTO log DEFAULT VALUES RETURNING id, insert_time;" test
    sleep 1
done
