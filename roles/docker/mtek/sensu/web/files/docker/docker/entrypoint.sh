#!/bin/bash
set -e

if [ "$1" = 'sensu-web' ]; then
    /docker/render.py --template /docker/conf/uchiwa.json --outfile /etc/sensu/uchiwa.json
    exec /opt/uchiwa/bin/uchiwa -c /etc/sensu/uchiwa.json -p /opt/uchiwa/src/public
fi

exec "$@"
