FROM ubuntu:trusty
MAINTAINER Massimiliano Ravelli, m.ravelli@mastervoice.it


# user and group
RUN groupadd -r -g 999 rabbitmq && useradd -r -d /var/lib/rabbitmq -m -u 999 -g 999 rabbitmq


# http://www.rabbitmq.com/install-debian.html
# "Please note that the word testing in this line refers to the state of our release of RabbitMQ, not any particular Debian distribution."
RUN apt-key adv --keyserver pool.sks-keyservers.net --recv-keys F78372A06FF50C80464FC1B4F7B8CEA6056E8E56 \
 && echo 'deb http://www.rabbitmq.com/debian/ testing main' > /etc/apt/sources.list.d/rabbitmq.list


# Required packages
ENV RABBITMQ_VERSION 3.4.3-1
RUN apt-get update && apt-get install -y python3-jinja2 rabbitmq-server=$RABBITMQ_VERSION --no-install-recommends && rm -rf /var/lib/apt/lists/*


# get logs to stdout (thanks to http://www.superpumpup.com/docker-rabbitmq-stdout for inspiration)
# TODO figure out what we'd need to do to add "(sasl_)?" to this sed and have it work ("{"init terminating in do_boot",{rabbit,failure_during_boot,{error,{cannot_log_to_tty,sasl_report_tty_h,not_installed}}}}")
RUN sed -E 's!^(\s*-rabbit\s+error_logger)\s+\S*!\1 tty!' /usr/lib/rabbitmq/lib/rabbitmq_server-*/sbin/rabbitmq-server > /tmp/rabbitmq-server \
    && chmod +x /tmp/rabbitmq-server \
    && mv /tmp/rabbitmq-server /usr/lib/rabbitmq/lib/rabbitmq_server-*/sbin/rabbitmq-server


# Enable management plugin
RUN rabbitmq-plugins enable --offline rabbitmq_management


COPY docker /docker

VOLUME ["/var/lib/rabbitmq", "/etc/rabbitmq/ssl"]

ENV default_vhost="/"
ENV default_user=admin
ENV default_pass=admin
ENV vhosts="[]"
ENV users="[]"


EXPOSE 5671 5672 15672

ENTRYPOINT ["/docker/entrypoint.sh"]
CMD ["rabbitmq-server"]
