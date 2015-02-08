FROM mtek/sensu-base
MAINTAINER Massimiliano Ravelli, m.ravelli@mastervoice.it


# Required packages
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y sensu


# /docker directory
COPY docker /docker
RUN chmod 0755 /docker/entrypoint.sh
RUN chmod 0755 /docker/render.py


ENV rabbitmq_ssl=false
ENV rabbitmq_password=sensu
ENV api_password=admin

VOLUME ["/etc/sensu/ssl"]
EXPOSE 4567

ENTRYPOINT ["/docker/entrypoint.sh"]
CMD ["sensu-api"]
