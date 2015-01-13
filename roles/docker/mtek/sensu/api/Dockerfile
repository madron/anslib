FROM sensu_base
MAINTAINER Massimiliano Ravelli, m.ravelli@mastervoice.it


ADD api.json /etc/sensu/api.json

CMD ["/opt/sensu/bin/sensu-api", "--config", "/etc/sensu/api.json"]
