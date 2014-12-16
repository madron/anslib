FROM mtek/postgres:9.3
MAINTAINER Massimiliano Ravelli, m.ravelli@mastervoice.it


# Sql schema
ADD docker/create_db.sql /docker/sql/init.sql
ADD docker/preseed.txt /docker/preseed.txt
RUN DEBIAN_FRONTEND=noninteractive \
       apt-get update \
    && apt-get install -y debconf-utils software-properties-common \
    && add-apt-repository ppa:formorer/icinga \
    && apt-get update \
    && debconf-set-selections < /docker/preseed.txt \
    && apt-get install -y icinga2-ido-pgsql \
    && cat /usr/share/dbconfig-common/data/icinga2-ido-pgsql/install/pgsql >> /docker/sql/init.sql \
    && apt-get --purge -y remove icinga2-ido-pgsql debconf-utils software-properties-common \
    && apt-get --purge -y autoremove \
    && apt-get clean \
    && apt-get autoclean
