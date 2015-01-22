#!/bin/bash
set -e

if [ "$1" = 'sensu-web' ]; then
    sed -i "s/REPLACE_HOST/$SENSU_API_HOST/g" /etc/sensu/uchiwa.json
    sed -i "s/REPLACE_PORT/$SENSU_API_PORT/g" /etc/sensu/uchiwa.json
    exec /opt/uchiwa/bin/uchiwa -c /etc/sensu/uchiwa.json -p /opt/uchiwa/src/public
fi

exec "$@"
