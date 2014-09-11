FROM ubuntu:trusty
MAINTAINER Massimiliano Ravelli, m.ravelli@mastervoice.it

# docker build -t mtek/celery roles/docker/mtek/celery/files/docker/


# Required packages
RUN DEBIAN_FRONTEND=noninteractive \
       apt-get update \
    && apt-get install -y python-pip \
    && apt-get install -y python-dev \
    && pip install celery[librabbitmq,redis] \
    && pip install flower \
    && apt-get --purge remove -y python-dev \
    && apt-get --purge autoremove -y

# Celery user and group
RUN groupadd --gid 999 celery
RUN useradd --home-dir /celery --create-home --uid 999 --gid 999 celery


WORKDIR /celery
