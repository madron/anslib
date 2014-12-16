FROM ubuntu:trusty
MAINTAINER Massimiliano Ravelli, m.ravelli@mastervoice.it


# User
RUN groupadd -g 999 nagios && useradd -u 999 -g 999 nagios


# Required packages
RUN DEBIAN_FRONTEND=noninteractive apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y software-properties-common
RUN add-apt-repository ppa:formorer/icinga
RUN DEBIAN_FRONTEND=noninteractive apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y icinga2


RUN mkdir -p /run/icinga2/cmd
RUN chown nagios.nagios /run/icinga2


CMD ["/usr/sbin/icinga2", "daemon"]
