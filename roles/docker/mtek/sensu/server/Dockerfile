FROM sensu_base
MAINTAINER Massimiliano Ravelli, m.ravelli@mastervoice.it


ADD server.json /etc/sensu/server.json

CMD ["/opt/sensu/bin/sensu-server", "--config", "/etc/sensu/server.json"]
