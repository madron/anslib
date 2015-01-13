FROM sensu_base
MAINTAINER Massimiliano Ravelli, m.ravelli@mastervoice.it

# Required packages
RUN DEBIAN_FRONTEND=noninteractive && apt-get install -y git ruby-dev build-essential
RUN gem install sensu-plugin --no-rdoc --no-ri
RUN git clone https://github.com/sensu/sensu-community-plugins.git /opt/community

ADD client.json /etc/sensu/client.json

CMD ["/opt/sensu/bin/sensu-client", "--config", "/etc/sensu/client.json"]
