FROM ubuntu:precise
MAINTAINER Massimiliano Ravelli, m.ravelli@mastervoice.it

# docker build -t mtek/postgres:precise .


# Postgres user and group
RUN groupadd -g 999 postgres
RUN useradd -d /var/lib/postgresql/9.1 -u 999 -g 999 postgres


# Required packages
RUN DEBIAN_FRONTEND=noninteractive apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y postgresql-9.1
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y sudo
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y nano less

RUN rm -rf /etc/postgresql/9.1/main
RUN rm -rf /var/lib/postgresql/9.1/main

# Config
RUN mkdir /docker
ADD entrypoint.sh /docker/entrypoint.sh
RUN chmod 755 /docker/entrypoint.sh
ADD pg_hba.conf /docker/
ADD pg_ident.conf /docker/
ADD postgresql.conf /docker/


EXPOSE 5432 5433
VOLUME ["/etc/postgresql/9.1", "/var/lib/postgresql/9.1"]


ENTRYPOINT ["/docker/entrypoint.sh"]
CMD ["postgres"]
