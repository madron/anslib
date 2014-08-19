#!/bin/bash

if [ -z "$1" ]; then
    export COUNT=1
else
    export COUNT=$1
fi


if [ -z "$2" ]; then
    export DELAY=1
else
    export DELAY=$2
fi


while true
do
    psql -h postgres -U postgres -c "DELETE FROM log WHERE id NOT IN (SELECT id FROM log ORDER BY id DESC LIMIT ${COUNT});" test
    sleep ${DELAY}
done
