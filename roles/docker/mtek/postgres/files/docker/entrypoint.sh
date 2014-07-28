#!/bin/bash
set -e

export VERSION=9.1
export PGDATA=/var/lib/postgresql/$VERSION
export POSTGRES=/usr/lib/postgresql/$VERSION/bin/postgres
export CONFIG_DIR=/etc/postgresql/$VERSION/main


if [[ "$1" = "postgres" ]]; then
    chown -R postgres "$PGDATA"

    if [ -z "$(ls -A "$PGDATA")" ]; then
        /usr/bin/pg_createcluster $VERSION main
        cp /docker/pg_hba.conf $CONFIG_DIR/
        cp /docker/pg_ident.conf $CONFIG_DIR/
        cp /docker/postgresql.conf $CONFIG_DIR/

        #sed -ri "s/^#(listen_addresses\s*=\s*)\S+/\1'*'/" "$PGDATA"/postgresql.conf
        # { echo; echo 'host all all 0.0.0.0/0 trust'; } >> "$PGDATA"/pg_hba.conf
    fi

    sudo -i -u postgres $POSTGRES -D $PGDATA/main -c config_file=$CONFIG_DIR/postgresql.conf

else
    exec "$@"
fi
