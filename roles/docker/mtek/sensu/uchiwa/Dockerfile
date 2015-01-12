FROM sensu_base
MAINTAINER Massimiliano Ravelli, m.ravelli@mastervoice.it


# Required packages
RUN DEBIAN_FRONTEND=noninteractive && apt-get install -y uchiwa


ADD uchiwa.json /etc/sensu/uchiwa.json
