# db data
docker run --name db_master_data -v /data busybox
docker run --name db_slave_data -v /data busybox

# remove db data
docker rm db_master_data
docker rm db_slave_data

# Run db_master server
docker run -i -t --rm --name db_master --volumes-from db_master_data -e WAL_KEEP_SEGMENTS=20 mtek/postgres:precise
docker run -d --name db_master --volumes-from db_master_data -e WAL_KEEP_SEGMENTS=20 mtek/postgres:precise

# Backup db to /tmp
docker run -i -t --rm --link db_master:postgres --volumes-from db_master  -v /tmp:/backup mtek/postgres:precise backup

# restore backup from /tmp to db_slave_data
# docker run -i -t --rm --volumes-from db_slave_data -v /tmp:/backup busybox tar xvf /backup/db_data.tar



# Run db_slave server
docker run -i -t --rm --name db_slave --link db_master:master -e MASTER_SERVER=master mtek/postgres:precise

# Create test database and log table
docker run -i -t --rm --link db_master:postgres mtek/postgres-test:precise /create-table.sh

# Insert 10Mb row every second
docker run -i -t --rm --name db_master_insert --link db_master:postgres mtek/postgres-test:precise /insert.sh 10000
docker run -i -t --rm --name db_master_insert --link db_master:postgres mtek/postgres-test:precise /insert.sh <size_in_kb>

# Keep only last 100 rows
docker run -i -t --rm --name db_master_delete --link db_master:postgres mtek/postgres-test:precise /delete.sh 100


# Check last row every second
docker run -i -t --rm --name db_master_select --link db_master:postgres mtek/postgres-test:precise /select.sh


# db_master utility container
docker run -i -t --rm --hostname db_master_util  --volumes-from db_master -v /tmp:/backup --link db_master:postgres mtek/postgres-test:precise bash


# http://www.postgresql.org/docs/9.1/static/continuous-archiving.html

psql -h postgres -U postgres

pg_controldata /data | grep checkpoint ; ls -l /data/pg_xlog/


# Start backup command
psql -h postgres -U postgres -c "SELECT pg_start_backup('label');"

# Manually backup data directory

# Stop backup command
psql -h postgres -U postgres -c "SELECT pg_stop_backup();"


psql -h postgres -U postgres -c "SELECT pg_start_backup('label');"
Wait
psql -h postgres -U postgres -c "VACUUM FULL;"
psql -h postgres -U postgres -c "REINDEX log;"
psql -h postgres -U postgres -c "CHECKPOINT;"
