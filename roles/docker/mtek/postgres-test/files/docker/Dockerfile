FROM mtek/postgres:9.1
MAINTAINER Massimiliano Ravelli, m.ravelli@mastervoice.it


# Packages
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y python-psycopg2
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y rdiff-backup


# Files
ADD docker /docker/
RUN chmod 755 /docker/*.sh
RUN chmod 755 /docker/*.py
