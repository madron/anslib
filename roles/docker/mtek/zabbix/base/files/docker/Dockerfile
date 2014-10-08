FROM ubuntu:trusty
MAINTAINER Massimiliano Ravelli, m.ravelli@mastervoice.it


# Required packages
RUN DEBIAN_FRONTEND=noninteractive \
       apt-get update \
    && apt-get install -y libcurl3 libcurl3-gnutls libiksemel3 libopenipmi0 libpq5 libsnmp30 libssh2-1 libxml2 debconf postgresql-client fping

# User
RUN groupadd -g 999 zabbix && useradd -d /zabbix -u 999 -g 999 zabbix

# Patch
ADD zabbix-TRUNK_r45165-run_foreground.patch /build/

# Install
RUN DEBIAN_FRONTEND=noninteractive \
       apt-get install -y build-essential curl libcurl4-gnutls-dev libiksemel-dev libopenipmi-dev libpq-dev libsnmp-dev libssh2-1-dev libxml2-dev \
    && curl -L http://sourceforge.net/projects/zabbix/files/ZABBIX%20Latest%20Stable/2.4.0/zabbix-2.4.0.tar.gz/download > /build/zabbix-2.4.0.tar.gz \
    && tar --directory /build -x -z -f /build/zabbix-2.4.0.tar.gz \
    && cd /build/zabbix-2.4.0 \
    && patch -p0 < /build/zabbix-TRUNK_r45165-run_foreground.patch \
    && ./configure --enable-server --enable-proxy --with-postgresql --enable-ipv6 --with-jabber --with-libxml2 --with-net-snmp --with-ssh2 --with-openipmi --with-libcurl \
    && make install \
    && apt-get -y --purge remove build-essential curl libcurl4-gnutls-dev libiksemel-dev libopenipmi-dev libpq-dev libsnmp-dev libssh2-1-dev libxml2-dev \
    && apt-get -y --purge autoremove \
    && rm -rf /build
