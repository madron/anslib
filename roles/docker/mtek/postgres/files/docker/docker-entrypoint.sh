#!/bin/bash
set -e

export VERSION=9.1
export PGDATA=/var/lib/postgresql/$VERSION
export POSTGRES=/usr/lib/postgresql/$VERSION/bin/postgres
export CONFIG_FILE=/etc/postgresql/$VERSION/main/postgresql.conf

echo ===$1===

if [[ "$1" = "postgres" ]]; then
    echo 'pppp'
    chown -R postgres "$PGDATA"

    if [ -z "$(ls -A "$PGDATA")" ]; then
        /usr/bin/pg_createcluster $VERSION main
        #sed -ri "s/^#(listen_addresses\s*=\s*)\S+/\1'*'/" "$PGDATA"/postgresql.conf
        # { echo; echo 'host all all 0.0.0.0/0 trust'; } >> "$PGDATA"/pg_hba.conf
    fi

    sudo -i -u postgres $POSTGRES -D $PGDATA/main -c config_file=$CONFIG_FILE

else
    exec "$@"
fi
