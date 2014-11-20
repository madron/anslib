# Build
docker build -t mtek/postgres-test roles/docker/mtek/postgres-test/files/docker/

# remove db data
docker rm -fv db_master_data_volume
docker rm -fv db_master_backup_volume

# db data
docker run --name db_master_data_volume -v /data busybox
docker run --name db_master_backup_volume -v /backup busybox

# Run db_master server
docker run -it --rm --name db_master --volumes-from db_master_data_volume --volumes-from db_master_backup_volume mtek/postgres-test

# Backup
docker exec -it db_master /docker/rdiff.sh


# Load data
docker run -it --rm --volumes-from db_master mtek/postgres-test sudo -i -u postgres /docker/load_bytea.py
