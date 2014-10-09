FROM mtek/postgres:9.3
MAINTAINER Massimiliano Ravelli, m.ravelli@mastervoice.it


# init.sql
ADD create_db.sql /docker/init.sql
RUN DEBIAN_FRONTEND=noninteractive \
       apt-get update \
    && apt-get install -y curl \
    && mkdir /build \
    && cd /build \
    && curl -L http://sourceforge.net/projects/zabbix/files/ZABBIX%20Latest%20Stable/2.4.0/zabbix-2.4.0.tar.gz/download | tar xz \
    && cd /build/zabbix-2.4.0/database/postgresql \
    && cp schema.sql /docker/ \
    && cp images.sql /docker/ \
    && cp data.sql   /docker/ \
    && cd /docker \
    && cat schema.sql >> init.sql \
    && cat images.sql >> init.sql \
    && cat data.sql   >> init.sql \
    && rm -rf /build \
    && apt-get install -y --purge remove curl
