FROM ubuntu:trusty
MAINTAINER Massimiliano Ravelli, m.ravelli@mastervoice.it

# user and group
RUN groupadd -r rabbitmq && useradd -r -d /var/lib/rabbitmq -m -g rabbitmq rabbitmq

# Required packages
RUN DEBIAN_FRONTEND=noninteractive && apt-get -y update && apt-get install -y rabbitmq-server

# get logs to stdout (thanks to http://www.superpumpup.com/docker-rabbitmq-stdout)
RUN grep -vE '^\s+-rabbit .*error_logger.*' /usr/lib/rabbitmq/lib/rabbitmq_server-*/sbin/rabbitmq-server >  /tmp/rabbitmq-server \
    && chmod +x /tmp/rabbitmq-server \
    && mv /tmp/rabbitmq-server /usr/lib/rabbitmq/lib/rabbitmq_server-*/sbin/rabbitmq-server
ENV RABBITMQ_SERVER_START_ARGS -eval error_logger:tty(true).

RUN rabbitmq-plugins enable rabbitmq_management

ADD docker-entrypoint.sh /
RUN chmod 0755 /docker-entrypoint.sh
ADD rabbitmq.config /etc/rabbitmq/rabbitmq.config


VOLUME ["/var/lib/rabbitmq", "/etc/rabbitmq/ssl"]

ENV RABBITMQ_VHOST=/
ENV RABBITMQ_USER=admin
ENV RABBITMQ_PASS=admin

EXPOSE 5671 5672 15672

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["rabbitmq-server"]
