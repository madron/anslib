#!/bin/bash

while true
do
    psql -h postgres -U postgres -c "select id, insert_time from log order by id desc limit 1;" test
    sleep 1
done
