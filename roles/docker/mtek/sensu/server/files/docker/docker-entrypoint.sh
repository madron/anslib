#!/bin/bash
set -e

if [ "$1" = 'sensu-server' ]; then
    sed -i "s/RABBITMQHOST/$RABBITMQ_HOST/g" /etc/sensu/server.json
    sed -i "s/RABBITMQPORT/$RABBITMQ_PORT/g" /etc/sensu/server.json
    sed -i "s/RABBITMQPASSWORD/$RABBITMQ_PASSWORD/g" /etc/sensu/server.json
    sed -i "s/APIPASSWORD/$API_PASSWORD/g" /etc/sensu/server.json
    exec /opt/sensu/bin/sensu-server --config /etc/sensu/server.json --config_dir /etc/sensu/conf.d
fi

exec "$@"
