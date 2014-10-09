#!/bin/bash
set -e

export VERSION=9.3
export PGBIN=/usr/lib/postgresql/${VERSION}/bin
export PGDATA=/data


chown -R postgres.postgres /var/run/postgresql
chmod 775 /var/run/postgresql

if [[ "$1" = "postgres" ]]; then
    chown -R postgres "${PGDATA}"

    # Create cluster if it doesn't exist
    if [ -z "$(ls -A "${PGDATA}")" ]; then
        sudo -i -u postgres ${PGBIN}/initdb --pgdata=${PGDATA} --encoding=UTF8
        rm ${PGDATA}/postgresql.conf
        rm ${PGDATA}/pg_hba.conf
        rm ${PGDATA}/pg_ident.conf
    fi
    # Config files
    # pg_hba.conf will be created only if it doesn't exist
    if [ ! -f "${PGDATA}/pg_hba.conf" ]; then
        /docker/render.py --template /docker/pg_hba.conf --outfile ${PGDATA}/pg_hba.conf
    fi
    # postgresql.conf is always overwritten
    /docker/render.py --template /docker/postgresql.conf --outfile ${PGDATA}/postgresql.conf
    # recovery.conf is always overwritten
    rm -f ${PGDATA}/recovery.conf
    if [ ! "${MASTER_SERVER}" == "" ]; then
        /docker/render.py --template /docker/recovery.conf --outfile ${PGDATA}/recovery.conf
    fi

    sudo -i -u postgres ${PGBIN}/postgres -D ${PGDATA} -c config_file=${PGDATA}/postgresql.conf

elif [[ "$1" = "syncuser" ]]; then
    psql -h postgres -U postgres -c "CREATE USER syncuser REPLICATION LOGIN CONNECTION LIMIT 1 ENCRYPTED PASSWORD '$2';"

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
