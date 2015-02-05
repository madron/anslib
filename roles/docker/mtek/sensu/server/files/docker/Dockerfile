FROM mtek/sensu-base
MAINTAINER Massimiliano Ravelli, m.ravelli@mastervoice.it


# Sensu user and group
RUN groupadd \
    --gid  999 \
    sensu \
 && useradd  \
    --uid 999 \
    --gid 999 \
    --comment "Sensu Monitoring Framework" \
    --home-dir /opt/sensu \
    --shell /bin/false \
    sensu

ENV PLUGIN_VERSION=5fdba6050f59f518073016849e33c097ad696914
ENV BASE_DIR=sensu-community-plugins-$PLUGIN_VERSION

# Required packages
RUN DEBIAN_FRONTEND=noninteractive \
       apt-get update \
    && apt-get install -y curl sensu

#     && wget -q http://repos.sensuapp.org/apt/pubkey.gpg -O- | sudo apt-key add - \
#     && echo "deb     http://repos.sensuapp.org/apt sensu main" > /etc/apt/sources.list.d/sensu.list \
#     && apt-get update \
#     && apt-get install -y sensu \
#     && gem install sensu-plugin --version=1.1.0 --no-rdoc --no-ri \
#     && curl -L -s -o /tmp/plugins.tgz https://github.com/sensu/sensu-community-plugins/archive/$PLUGIN_VERSION.tar.gz \
#     && apt-get -y --purge remove wget curl ruby-dev build-essential \
#     && apt-get -y --purge autoremove \
#     && cd /etc/sensu/ \
#     && tar --strip-components 1 -x -z -f /tmp/plugins.tgz $BASE_DIR/extensions $BASE_DIR/handlers $BASE_DIR/mutators $BASE_DIR/plugins $BASE_DIR/scripts $BASE_DIR/spec \
#     && rm /tmp/plugins.tgz


ADD ruby-sensu-plugin_1.1.0-1_all.deb /var/cache/apt/archives/
RUN dpkg -i /var/cache/apt/archives/ruby-sensu-plugin_1.1.0-1_all.deb

#RUN gem install sentry-raven==0.12.3

RUN curl -L -s -o /tmp/sensu-plugins.tgz https://github.com/sensu/sensu-community-plugins/archive/-$PLUGIN_VERSION.tar.gz
RUN cd /etc/sensu/ \
    && tar --strip-components 1 -x -z -f /tmp/plugins.tgz $BASE_DIR/extensions $BASE_DIR/handlers $BASE_DIR/mutators $BASE_DIR/plugins

# ADD docker-entrypoint.sh /
# RUN chmod 0755 /docker-entrypoint.sh
# ADD server.json /etc/sensu/server.json
#
# VOLUME ["/etc/sensu/ssl", "/etc/sensu/conf.d"]
#
# ENTRYPOINT ["/docker-entrypoint.sh"]
# CMD ["sensu-server"]
