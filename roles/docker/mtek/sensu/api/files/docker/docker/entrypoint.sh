#!/bin/bash
set -e

if [ "$1" = 'sensu-api' ]; then
    /docker/render.py --template /docker/conf/api.json --outfile /etc/sensu/api.json
    exec /opt/sensu/bin/sensu-api --config /etc/sensu/api.json
fi

exec "$@"
