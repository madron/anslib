FROM ubuntu:precise
MAINTAINER Massimiliano Ravelli, m.ravelli@mastervoice.it

# docker build -t mtek/postgres-test:precise .


# Required packages
RUN DEBIAN_FRONTEND=noninteractive apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y postgresql-client
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y sudo
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y nano less


# Scripts
ADD create-table.sh /
ADD insert.sh /
ADD select.sh /

RUN chmod 755 /*.sh
