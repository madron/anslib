#!/bin/bash
set -e

if [ "$1" = 'rabbitmq-server' ]; then
    chown -R rabbitmq /var/lib/rabbitmq
    # Escape RABBITMQ_VHOST for sed
    RABBITMQ_VHOST="${RABBITMQ_VHOST//\//\\/}"
    sed -i "s/RABBITMQ_VHOST/$RABBITMQ_VHOST/g" /etc/rabbitmq/rabbitmq.config
    sed -i "s/RABBITMQ_USER/$RABBITMQ_USER/g"   /etc/rabbitmq/rabbitmq.config
    sed -i "s/RABBITMQ_PASS/$RABBITMQ_PASS/g"   /etc/rabbitmq/rabbitmq.config
fi

exec "$@"
