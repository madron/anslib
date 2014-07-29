#!/bin/bash

while true
do
    psql -h postgres -U postgres -c "INSERT INTO log DEFAULT VALUES RETURNING id, insert_time;" test | grep "\."
    sleep 1
done
