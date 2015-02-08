#!/bin/bash
set -e

if [ "$1" = 'rabbitmq-server' ]; then
    chown -R rabbitmq /var/lib/rabbitmq
    # Start temporary rabbitmq server with no exposed ports
    /docker/render.py --template /docker/conf/rabbitmq-local.config --outfile /etc/rabbitmq/rabbitmq.config
    /etc/init.d/rabbitmq-server start
    # Add vhosts and users
    /docker/add_vhosts.py
    /docker/add_users.py
    # Stop temporary rabbitmq server
    /etc/init.d/rabbitmq-server stop
    epmd -kill
    # Standard configuration
    /docker/render.py --template /docker/conf/rabbitmq.config --outfile /etc/rabbitmq/rabbitmq.config
fi

exec "$@"
