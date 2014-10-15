#!/bin/bash
set -e

export VERSION=9.3
export PGBIN=/usr/lib/postgresql/${VERSION}/bin


chown -R postgres.postgres /var/run/postgresql
chmod 775 /var/run/postgresql

if [[ "$1" = "postgres" ]]; then
    chown -R postgres "/data"

    # Create cluster if it doesn't exist
    if [ -z "$(ls -A "/data")" ]; then
        sudo -i -u postgres ${PGBIN}/initdb --pgdata=/data --encoding=UTF8
        # Config files
        rm /data/pg_ident.conf
        /docker/render.py --template /docker/conf/postgresql.conf --outfile /data/postgresql.conf
        /docker/render.py --template /docker/conf/pg_hba.conf --outfile /data/pg_hba.conf
        # Init sql
        if [ -f "/docker/sql/init.sql" ]; then
            echo "Loading init.sql"
            sudo -i -u postgres pg_ctl start -w -D /data --silent -o "-c listen_addresses=''"
            sudo -i -u postgres psql -f /docker/sql/init.sql
            sudo -i -u postgres pg_ctl stop -w -D /data --silent
        fi
    fi

    # pg_hba.conf  is always overwritten
    /docker/render.py --template /docker/conf/pg_hba.conf --outfile /data/pg_hba.conf

    # recovery.conf is always overwritten
    rm -f /data/recovery.conf
    if [ ! "${master_server}" == "" ]; then
        /docker/render.py --template /docker/conf/recovery.conf --outfile /data/recovery.conf
    fi

    # Start postgres
    echo "Starting postgres"
    exec sudo -i -u postgres exec ${PGBIN}/postgres -D /data -c config_file=/data/postgresql.conf

elif [[ "$1" = "pg_hba" ]]; then
    /docker/render.py --template /docker/conf/pg_hba.conf --outfile /data/pg_hba.conf
    exec sudo -i -u postgres psql -c "SELECT pg_reload_conf();" > /dev/null

elif [[ "$1" = "psql" ]]; then
    exec sudo -i -u postgres "$@"

elif [[ "$1" = "syncuser" ]]; then
    exec sudo -i -u postgres psql -c "CREATE USER syncuser REPLICATION LOGIN CONNECTION LIMIT 1 ENCRYPTED PASSWORD '$2';"

elif [[ "$1" = "backup" ]]; then
    if [[ "$2" = "--overwrite" ]]; then
        rm -rf /backup/pg_basebackup
        rm -f /backup/base.tar.gz
    fi
    if [ -f "/backup/base.tar.gz" ]; then
        # Abort if file exists
        echo "File /backup/base.tar.gz already exists."
        exit 1
    fi
    if [ -d "/backup/pg_basebackup" ]; then
        # Abort if working directory exists
        echo "Working directory /backup/pg_basebackup already exists: maybe another backup is running."
        exit 1
    fi
    rm -rf /backup/pg_basebackup
    mkdir /backup/pg_basebackup
    chown postgres /backup/pg_basebackup
    sudo -i -u postgres ${PGBIN}/pg_basebackup --pgdata=/backup/pg_basebackup --xlog --format=tar --progress --verbose
    gzip --rsyncable --stdout /backup/pg_basebackup/base.tar > /backup/base.tar.gz
    rm -rf /backup/pg_basebackup

elif [[ "$1" = "restore" ]]; then
    # Check if backup exists
    if [ ! -f "/backup/base.tar.gz" ]; then
        echo "File /backup/base.tar.gz doesn't exist."
        exit 1
    fi
    # Check if postgres is running
    if [ -S "/var/run/postgresql/.s.PGSQL.5432" ]; then
        echo "Found postgres running: aborting."
        exit 1
    fi
    # Remove old data and restore
    cd /data
    rm -rf *
    tar xfz /backup/base.tar.gz
else
    exec "$@"
fi
