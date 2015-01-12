FROM ubuntu:trusty
MAINTAINER Massimiliano Ravelli, m.ravelli@mastervoice.it


# User
RUN groupadd -g 999 nagios && useradd -u 999 -g 999 nagios


# Required packages
ADD docker/preseed.txt /docker/preseed.txt
RUN DEBIAN_FRONTEND=noninteractive apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y debconf-utils software-properties-common
RUN add-apt-repository ppa:formorer/icinga
RUN DEBIAN_FRONTEND=noninteractive apt-get update
RUN debconf-set-selections < /docker/preseed.txt
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y icinga2 icinga2-ido-pgsql


# Configuration
RUN mkdir -p /run/icinga2/cmd
RUN chown -R nagios.nagios /run/icinga2
ADD docker/ido-pgsql.conf /etc/icinga2/features-available/ido-pgsql.conf
RUN icinga2 feature enable ido-pgsql
RUN icinga2 feature enable command
RUN icinga2 feature enable livestatus

VOLUME ["/run/icinga2/cmd"]

CMD ["/usr/sbin/icinga2", "daemon"]
