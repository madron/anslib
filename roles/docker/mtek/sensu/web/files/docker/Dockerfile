FROM mtek/sensu-base
MAINTAINER Massimiliano Ravelli, m.ravelli@mastervoice.it


# Required packages
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y uchiwa


# /docker directory
COPY docker /docker
RUN chmod 0755 /docker/entrypoint.sh
RUN chmod 0755 /docker/render.py

ENV servers='[{"name": "Sensu", "port": 4567, "host": "api", "password": "admin", "username": "admin", "slug": "sensu"}]'
ENV username=''
ENV password=''

EXPOSE 3000

ENTRYPOINT ["/docker/entrypoint.sh"]
CMD ["sensu-web"]
