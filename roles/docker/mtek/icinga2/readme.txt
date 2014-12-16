docker build -t mtek/icinga2-db roles/docker/mtek/icinga2/db/files/docker/
docker build -t mtek/icinga2-server roles/docker/mtek/icinga2/server/files/docker/


docker run -d --name icinga_db -e allowed_networks=172.17.0.0/16 mtek/icinga2-db
docker run -it --rm --link icinga_db:db mtek/icinga2-server
