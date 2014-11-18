# Build
docker build -t mtek/postgres-test roles/docker/mtek/postgres-test/files/docker/

# remove db data
docker rm db_master_data_volume
docker rm db_master_backup_volume

# db data
docker run --name db_master_data_volume -v /data busybox
docker run --name db_master_backup_volume -v /backup busybox

# Run db_master server
docker run -it --rm --name db_master --volumes-from db_master_data_volume --volumes-from db_master_backup_volume mtek/postgres-test

# Backup
docker exec -it db_master /docker/rdiff.sh
docker exec -it db_master ls -lh /backup
docker exec -it db_master bash



# restore backup from ~/tmp
docker run -it --rm --volumes-from db_master_data_volume -v ~/tmp:/backup busybox cp -a /backup/data /


# Create database and schema
docker run -it --rm --volumes-from db_master mtek/postgres-test psql -f /sql/schema.sql



docker run -it --rm --volumes-from db_master mtek/postgres-test sudo -i -u postgres /docker/load_bytea.py



# Insert 10Mb row every second
docker run -it --rm --name db_master_insert --volumes-from db_master mtek/postgres-test /insert.sh 10000
docker run -it --rm --name db_master_insert --volumes-from db_master mtek/postgres-test /insert.sh <size_in_kb>

# Keep only last 100 rows
docker run -it --rm --name db_master_delete --volumes-from db_master mtek/postgres-test /delete.sh 100


# Check last row every second
docker run -it --rm --name db_master_select --volumes-from db_master mtek/postgres-test /select.sh


# utility container
docker run -it --rm --hostname db_master_util --volumes-from db_master -v /tmp:/backup --volumes-from db_master mtek/postgres-test bash
docker run -it --rm --hostname db_backup_util --volumes-from db_backup -v /tmp:/backup --link db_backup:postgres mtek/postgres-test bash
docker run -it --rm --hostname db_slave_util  --volumes-from db_slave  -v /tmp:/backup --link db_slave:postgres  mtek/postgres-test bash
