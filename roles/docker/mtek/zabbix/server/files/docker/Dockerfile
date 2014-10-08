FROM mtek/zabbix_base:2.4
MAINTAINER Massimiliano Ravelli, m.ravelli@mastervoice.it


ADD docker /docker/


EXPOSE 10051


ENTRYPOINT ["zabbix_server", "--foreground", "--config", "/docker/zabbix_server.conf"]
