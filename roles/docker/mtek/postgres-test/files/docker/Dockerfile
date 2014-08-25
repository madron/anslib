FROM mtek/postgres:precise
MAINTAINER Massimiliano Ravelli, m.ravelli@mastervoice.it

# docker build -t mtek/postgres-test:precise roles/docker/mtek/postgres-test/files/docker/

# Scripts
ADD create-table.sh /
ADD insert.sh /
ADD select.sh /
ADD delete.sh /

RUN chmod 755 /*.sh
