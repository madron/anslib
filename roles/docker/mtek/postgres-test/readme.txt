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
docker run -it --rm --volumes-from db_master mtek/postgres-test /docker/rdiff.sh


# Load data
docker run -it --rm --volumes-from db_master mtek/postgres-test /docker/data.sh lobj insert
docker build -t mtek/postgres-test roles/docker/mtek/postgres-test/files/docker/ && docker run -it --rm --volumes-from db_master mtek/postgres-test /docker/data.sh lobj insert


# Psql
docker run -it --rm --volumes-from db_master mtek/postgres-test psql -c "SELECT COUNT(*) FROM bytea;" test


### Before every scenario
docker rm -fv db_master_volume
docker run --name db_master_volume -v /data -v /backup busybox
docker run -it --rm --name db_master --volumes-from db_master_volume mtek/postgres-test

### Scenario 1 (bytea)
docker run -it --rm --volumes-from db_master mtek/postgres-test /docker/rdiff.sh
docker run -it --rm --volumes-from db_master mtek/postgres-test /docker/data.sh bytea insert --files 100
docker run -it --rm --volumes-from db_master mtek/postgres-test /docker/rdiff.sh
docker run -it --rm --volumes-from db_master mtek/postgres-test /docker/rdiff.sh
docker run -it --rm --volumes-from db_master mtek/postgres-test /docker/data.sh bytea delete --id 20
docker run -it --rm --volumes-from db_master mtek/postgres-test /docker/rdiff.sh
docker run -it --rm --volumes-from db_master mtek/postgres-test /docker/rdiff.sh
docker run -it --rm --volumes-from db_master mtek/postgres-test /docker/data.sh bytea update --id 50
docker run -it --rm --volumes-from db_master mtek/postgres-test /docker/rdiff.sh
docker run -it --rm --volumes-from db_master mtek/postgres-test /docker/rdiff.sh
docker run -it --rm --volumes-from db_master mtek/postgres-test psql -c "VACUUM FULL;" test
docker run -it --rm --volumes-from db_master mtek/postgres-test /docker/rdiff.sh

### Scenario 2 (lobj)
docker run -it --rm --volumes-from db_master mtek/postgres-test /docker/rdiff.sh
docker run -it --rm --volumes-from db_master mtek/postgres-test /docker/data.sh lobj insert --files 100
docker run -it --rm --volumes-from db_master mtek/postgres-test /docker/rdiff.sh
docker run -it --rm --volumes-from db_master mtek/postgres-test /docker/rdiff.sh
docker run -it --rm --volumes-from db_master mtek/postgres-test /docker/data.sh lobj delete --id 20
docker run -it --rm --volumes-from db_master mtek/postgres-test /docker/rdiff.sh
docker run -it --rm --volumes-from db_master mtek/postgres-test /docker/rdiff.sh
docker run -it --rm --volumes-from db_master mtek/postgres-test /docker/data.sh lobj update --id 50
docker run -it --rm --volumes-from db_master mtek/postgres-test /docker/rdiff.sh
docker run -it --rm --volumes-from db_master mtek/postgres-test /docker/rdiff.sh
docker run -it --rm --volumes-from db_master mtek/postgres-test psql -c "VACUUM FULL;" test
docker run -it --rm --volumes-from db_master mtek/postgres-test /docker/rdiff.sh
