FROM ubuntu:trusty
MAINTAINER Massimiliano Ravelli, m.ravelli@mastervoice.it


# Postgres user and group
RUN groupadd -g 999 postgres && useradd -d /var/lib/postgresql/9.3 -u 999 -g 999 postgres


# Required packages
RUN DEBIAN_FRONTEND=noninteractive \
       apt-get update \
    && apt-get install -y postgresql-9.3 postgresql-client sudo python-jinja2 \
    && rm -rf /etc/postgresql/9.3/main \
    && rm -rf /var/lib/postgresql/9.3/main \
    && ln -s /usr/lib/postgresql/9.3/bin/* /usr/local/bin


# Config
ADD docker /docker/
RUN chmod 755 /docker/entrypoint.sh
RUN chmod 755 /docker/render.py


EXPOSE 5432
VOLUME ["/data"]
VOLUME ["/var/run/postgresql"]


ENTRYPOINT ["/docker/entrypoint.sh"]
CMD ["postgres"]
