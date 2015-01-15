#!/bin/bash
set -e

if [ "$1" = 'rabbitmq-server' ]; then
    chown -R rabbitmq /var/lib/rabbitmq
    sed -i "s/REPLACEME/$RABBITMQ_PASSWORD/g" /etc/rabbitmq/rabbitmq.config
fi

exec "$@"
