FROM sensu_base
MAINTAINER Massimiliano Ravelli, m.ravelli@mastervoice.it


# Required packages
RUN DEBIAN_FRONTEND=noninteractive && apt-get install -y uchiwa

ADD uchiwa.json /etc/sensu/uchiwa.json

CMD ["/opt/uchiwa/bin/uchiwa", "-c", "/etc/sensu/uchiwa.json", "-p", "/opt/uchiwa/src/public"]
