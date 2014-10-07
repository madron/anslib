FROM ubuntu:trusty
MAINTAINER Massimiliano Ravelli, m.ravelli@mastervoice.it


# Required packages
RUN DEBIAN_FRONTEND=noninteractive apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y libcurl3 libiksemel3 libopenipmi0 libpq5 libsnmp30 libssh2-1 libxml2 debconf postgresql-client fping

# User
RUN groupadd -g 999 zabbix
RUN useradd -d /zabbix -u 999 -g 999 zabbix



# Download source
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y build-essential curl libcurl4-gnutls-dev libiksemel-dev libopenipmi-dev libpq-dev libsnmp-dev libssh2-1-dev libxml2-dev
RUN mkdir /build
RUN curl -L http://sourceforge.net/projects/zabbix/files/ZABBIX%20Latest%20Stable/2.4.0/zabbix-2.4.0.tar.gz/download > /build/zabbix-2.4.0.tar.gz
RUN tar --directory /build -x -z -f /build/zabbix-2.4.0.tar.gz

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y nano

ADD zabbix-TRUNK_r45165-run_foreground.patch /build/

RUN cd /build/zabbix-2.4.0 ; patch -p0 < /build/zabbix-TRUNK_r45165-run_foreground.patch

RUN cd /build/zabbix-2.4.0 ; ./configure --enable-server --with-postgresql --enable-ipv6 --with-jabber --with-libxml2 --with-net-snmp --with-ssh2 --with-openipmi --with-libcurl
RUN cd /build/zabbix-2.4.0 ; make install


ADD docker /docker/


EXPOSE 10051


ENTRYPOINT ["zabbix_server", "--foreground", "--config", "/docker/zabbix_server.conf"]
# ENTRYPOINT ["bash"]








# # Required packages
# RUN DEBIAN_FRONTEND=noninteractive apt-get update
# RUN DEBIAN_FRONTEND=noninteractive apt-get install -y software-properties-common
#
#
# # Zabbix package
# RUN DEBIAN_FRONTEND=noninteractive apt-key adv --fetch-keys http://repo.zabbix.com/zabbix-official-repo.key
# RUN DEBIAN_FRONTEND=noninteractive add-apt-repository 'deb http://repo.zabbix.com/zabbix/2.4/ubuntu trusty main'
# RUN DEBIAN_FRONTEND=noninteractive apt-get update
# RUN echo "zabbix-server-pgsql zabbix-server-pgsql/dbconfig-install boolean false" | debconf-set-selections
# RUN DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends zabbix-server-pgsql
#
#
# RUN mkdir /var/run/zabbix
# RUN chown zabbix.zabbix /var/run/zabbix
#
#
# # Config
# ADD docker /docker/
#
# # RUN chmod 755 /docker/entrypoint.sh
# # RUN chmod 755 /docker/render.py
#
#
# EXPOSE 10051
#
#
# ENTRYPOINT ["zabbix_server", "--config", "/docker/zabbix_server.conf"]
# ENTRYPOINT ["bash"]
