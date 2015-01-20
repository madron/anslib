#!/bin/bash
set -e

if [ "$1" = 'sensu-server' ]; then
    sed -i "s/REPLACEME/$RABBITMQ_PASSWORD/g" /etc/sensu/server.json
    exec /opt/sensu/bin/sensu-server --config /etc/sensu/server.json
fi

exec "$@"
