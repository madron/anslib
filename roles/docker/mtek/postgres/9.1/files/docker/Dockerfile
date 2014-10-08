FROM ubuntu:precise
MAINTAINER Massimiliano Ravelli, m.ravelli@mastervoice.it


# Postgres user and group
RUN groupadd -g 999 postgres && useradd -d /var/lib/postgresql/9.1 -u 999 -g 999 postgres


# Required packages
RUN DEBIAN_FRONTEND=noninteractive \
       apt-get update \
    && apt-get install -y postgresql-9.1 postgresql-client sudo python-jinja2 \
    && rm -rf /etc/postgresql/9.1/main \
    && rm -rf /var/lib/postgresql/9.1/main \
    && ln -s /usr/lib/postgresql/9.1/bin/* /usr/local/bin


# Config
ADD docker /docker/
RUN chmod 755 /docker/entrypoint.sh
RUN chmod 755 /docker/render.py


EXPOSE 5432
VOLUME ["/data"]


ENTRYPOINT ["/docker/entrypoint.sh"]
CMD ["postgres"]
