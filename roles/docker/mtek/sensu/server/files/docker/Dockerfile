FROM mtek/sensu-base
MAINTAINER Massimiliano Ravelli, m.ravelli@mastervoice.it


# Required packages
RUN DEBIAN_FRONTEND=noninteractive \
       apt-get install -y curl sensu ruby libmixlib-cli-ruby ruby-dev build-essential


# Sensu community plugins
ENV PLUGIN_VERSION=5fdba6050f59f518073016849e33c097ad696914
ENV BASE_DIR=sensu-community-plugins-$PLUGIN_VERSION
RUN \
       curl -L -s -o /tmp/plugins.tgz https://github.com/sensu/sensu-community-plugins/archive/$PLUGIN_VERSION.tar.gz \
    && cd /etc/sensu/ \
    && tar --strip-components 1 -x -z -f /tmp/plugins.tgz $BASE_DIR/extensions $BASE_DIR/handlers $BASE_DIR/mutators $BASE_DIR/plugins \
    && rm /tmp/plugins.tgz


# Install gems
RUN gem install sentry-raven --version 0.12.3
RUN gem install influxdb --version 0.1.8


# sensu-plugin
ADD ruby-sensu-plugin_1.1.0-1_all.deb /var/cache/apt/archives/
RUN dpkg -i /var/cache/apt/archives/ruby-sensu-plugin_1.1.0-1_all.deb


# /docker directory
COPY docker /docker
RUN chmod 0755 /docker/entrypoint.sh
RUN chmod 0755 /docker/render.py


# Custom components
ADD sensu /etc/sensu/

ENV rabbitmq_ssl=false
ENV rabbitmq_password=sensu
ENV api_password=admin

VOLUME ["/etc/sensu/ssl", "/etc/sensu/conf.d"]

ENTRYPOINT ["/docker/entrypoint.sh"]
CMD ["sensu-server"]
