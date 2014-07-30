# Run db_master server
docker run -i -t --rm --name db_master mtek/postgres:precise

# Create test database and log table
docker run -i -t --rm --link db_master:postgres mtek/postgres-test:precise /create-table.sh

# Insert 1 row every second
docker run -i -t --rm --name db_master_insert --link db_master:postgres mtek/postgres-test:precise /insert.sh

# Check last row every second
docker run -i -t --rm --name db_master_select --link db_master:postgres mtek/postgres-test:precise /select.sh


# db_master utility container
docker run -i -t --rm --hostname db_master_util  --volumes-from db_master --link db_master:postgres mtek/postgres-test:precise bash


# http://www.postgresql.org/docs/9.1/static/continuous-archiving.html

psql -h postgres -U postgres

pg_controldata /data | grep checkpoint ; ls -l /data/pg_xlog/


# Start backup command
psql -h postgres -U postgres -c "SELECT pg_start_backup('label');"

# Manually backup data directory

# Stop backup command
psql -h postgres -U postgres -c "SELECT pg_stop_backup();"
