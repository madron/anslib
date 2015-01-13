FROM sensu_base
MAINTAINER Massimiliano Ravelli, m.ravelli@mastervoice.it


ADD client.json /etc/sensu/client.json

CMD ["/opt/sensu/bin/sensu-client", "--config", "/etc/sensu/client.json"]
