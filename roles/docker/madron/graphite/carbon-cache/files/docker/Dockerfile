FROM ubuntu:trusty
MAINTAINER Massimiliano Ravelli, massimiliano.ravelli@gmail.com


# Required packages
RUN DEBIAN_FRONTEND=noninteractive apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y python-pip python-dev

# Installation
RUN pip install https://github.com/graphite-project/ceres/tarball/master
RUN pip install whisper
RUN pip install https://github.com/graphite-project/carbon/tarball/master

# Config
ADD conf/* /opt/graphite/conf/


VOLUME ["/opt/graphite/storage"]

EXPOSE 2003 2004 7002

CMD ["/opt/graphite/bin/carbon-cache.py", "--nodaemon", "start"]
