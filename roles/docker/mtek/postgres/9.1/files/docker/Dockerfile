FROM postgres:9.1
MAINTAINER Massimiliano Ravelli, m.ravelli@mastervoice.it


# Required packages
RUN DEBIAN_FRONTEND=noninteractive \
       apt-get update \
    && apt-get install -y python-jinja2 python-netaddr \
    && rm -rf /var/lib/apt/lists/*


RUN rm -rf /docker-entrypoint-initdb.d \
 && rm docker-entrypoint.sh

# Config
ADD docker /docker/
RUN chmod 755 /docker/entrypoint.sh \
 && chmod 755 /docker/render.py


# Ephemeral volumes
# Needed to connect to postgres via unix socket
VOLUME ["/var/run/postgresql"]

EXPOSE 5432

ENTRYPOINT ["/docker/entrypoint.sh"]
CMD ["postgres"]
