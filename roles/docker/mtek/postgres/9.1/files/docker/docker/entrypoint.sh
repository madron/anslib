#!/bin/bash
set -e

chown -R postgres.postgres /var/run/postgresql
chmod 775 /var/run/postgresql

if [ "$1" = 'postgres' ]; then
    chown -R postgres "$PGDATA"

    # Create cluster if it doesn't exist
    if [ -z "$(ls -A "$PGDATA")" ]; then
        gosu postgres initdb --encoding=UTF8

        # Config files
        /docker/render.py --template /docker/conf/postgresql.conf --outfile $PGDATA/postgresql.conf
        /docker/render.py --template /docker/conf/pg_hba.conf --outfile $PGDATA/pg_hba.conf

        # Postgres password
        if [ "$POSTGRES_PASSWORD" ]; then
            echo ALTER USER "postgres" WITH SUPERUSER PASSWORD '$POSTGRES_PASSWORD'; > $PGDATA/init.sql
            gosu postgres postgres --single -jE < $PGDATA/init.sql
            rm $PGDATA/init.sql
        fi

        if [ "$allowed_replication_networks" ]; then
            # CREATE USER syncuser REPLICATION LOGIN CONNECTION LIMIT 1 ENCRYPTED PASSWORD '$2';
            echo "CREATE USER syncuser REPLICATION;" > $PGDATA/init.sql
            gosu postgres postgres --single -jE < $PGDATA/init.sql
            rm $PGDATA/init.sql
        fi

        # init.sql file
        if [ -f "/docker/sql/init.sql" ]; then
            echo "Loading init.sql"
            gosu postgres postgres --single -jE < /docker/sql/init.sql
        fi

        # initdb.d directory
        if [ -d /docker/initdb.d ]; then
            for f in /docker/initdb.d/*.sh; do
                [ -f "$f" ] && . "$f"
            done
        fi

        # INIT_SQL environment variable
        if [ "$INIT_SQL" ]; then
            echo $INIT_SQL > $PGDATA/init.sql
            gosu postgres postgres --single -jE < $PGDATA/init.sql
            rm $PGDATA/init.sql
        fi
    fi

    # Remove postgresql.conf from $PGDATA and it will be overwritten
    if [ ! -f "$PGDATA/postgresql.conf" ]; then
        echo "postgresql.conf file not present: regenerating standard one."
        /docker/render.py --template /docker/conf/postgresql.conf --outfile $PGDATA/postgresql.conf
    fi

    # pg_hba.conf  is always overwritten
    /docker/render.py --template /docker/conf/pg_hba.conf --outfile $PGDATA/pg_hba.conf

    # recovery.conf is always overwritten
    rm -f $PGDATA/recovery.conf
    if [ ! "${master_server}" == "" ]; then
        /docker/render.py --template /docker/conf/recovery.conf --outfile $PGDATA/recovery.conf
    fi

    # Start postgres
    echo "Starting postgres"
    exec gosu postgres postgres

elif [[ "$1" = "pg_hba" ]]; then
    /docker/render.py --template /docker/conf/pg_hba.conf --outfile $PGDATA/pg_hba.conf
    exec gosu postgres psql -c "SELECT pg_reload_conf();" > /dev/null

elif [[ "$1" = "psql" ]]; then
    exec gosu postgres "$@"

elif [[ "$1" = "syncuser" ]]; then
    exec gosu postgres psql -c "CREATE USER syncuser REPLICATION LOGIN CONNECTION LIMIT 1 ENCRYPTED PASSWORD '$2';"

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
    gosu postgres pg_basebackup --pgdata=/backup/pg_basebackup --xlog --format=tar --progress --verbose
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
    cd $PGDATA
    rm -rf *
    tar xfz /backup/base.tar.gz

else
    exec "$@"
fi
