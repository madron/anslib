FROM ubuntu:trusty
MAINTAINER Massimiliano Ravelli, m.ravelli@mastervoice.it

# docker build -t mtek/celery roles/docker/mtek/celery/files/docker/


# Required packages
RUN DEBIAN_FRONTEND=noninteractive apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y python-pip
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y python-dev
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y nano
RUN pip install celery[librabbitmq,redis]
RUN pip install flower

# Celery user and group
RUN groupadd -g 999 celery
RUN useradd -d /data -u 999 -g 999 celery



VOLUME ["/data"]


WORKDIR /data
