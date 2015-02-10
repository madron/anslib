#!/bin/bash
set -e

if [ "$1" = 'sensu-server' ]; then
    /docker/render.py --template /docker/conf/server.json --outfile /etc/sensu/server.json
    exec /opt/sensu/bin/sensu-server --config /etc/sensu/server.json --config_dir /etc/sensu/conf.d
fi

exec "$@"
