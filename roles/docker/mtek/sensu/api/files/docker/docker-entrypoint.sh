#!/bin/bash
set -e

if [ "$1" = 'sensu-api' ]; then
    sed -i "s/REPLACEME/$RABBITMQ_PASSWORD/g" /etc/sensu/api.json
    exec /opt/sensu/bin/sensu-api --config /etc/sensu/api.json
fi

exec "$@"
