#!/bin/bash
set -e

export VERSION=9.1
export PGBIN=/usr/lib/postgresql/${VERSION}/bin
export PGDATA=/data
export DATA_FILE=/docker/data.py
export DATA_DEFAULT=/docker/default_data.py


echo "data=dict()" >  $DATA_FILE
echo "data['WAL_KEEP_SEGMENTS']='$WAL_KEEP_SEGMENTS'" >>  $DATA_FILE
cat $DATA_DEFAULT >> $DATA_FILE

if [[ "$1" = "postgres" ]]; then
    chown -R postgres "${PGDATA}"

    # Create cluster if it doesn't exist
    if [ -z "$(ls -A "${PGDATA}")" ]; then
        sudo -i -u postgres ${PGBIN}/initdb --pgdata=${PGDATA} --encoding=UTF8
    fi

    # Config files
    mkdir -p "${PGDATA}"/etc
    # pg_hba.conf will be created only if it doesn't exist
    if [ ! -f "${PGDATA}/etc/pg_hba.conf" ]; then
        /docker/render.py --template /docker/pg_hba.conf --outfile ${PGDATA}/etc/pg_hba.conf
    fi
    # postgresql.conf is always overwritten
    /docker/render.py --template /docker/postgresql.conf --outfile ${PGDATA}/etc/postgresql.conf

    sudo -i -u postgres ${PGBIN}/postgres -D ${PGDATA} -c config_file=${PGDATA}/etc/postgresql.conf

else
    exec "$@"
fi
