#!/bin/bash

if [ -z "$1" ]; then
    export SIZE=1
else
    export SIZE=$1
fi


if [ -z "$2" ]; then
    export DELAY=1
else
    export DELAY=$2
fi


while true
do
    psql -h postgres -U postgres -c "INSERT INTO log (data) VALUES (repeat('1234567890ABCDEF', 64 * ${SIZE} )) RETURNING id, insert_time, char_length(data);" test | grep "\."
    sleep ${DELAY}
done
