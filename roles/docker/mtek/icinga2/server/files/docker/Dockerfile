FROM ubuntu:trusty
MAINTAINER Massimiliano Ravelli, m.ravelli@mastervoice.it


# User
RUN groupadd -g 999 icinga && useradd -u 999 -g 999 icinga


# Required packages
RUN DEBIAN_FRONTEND=noninteractive apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y software-properties-common
RUN add-apt-repository ppa:formorer/icinga
RUN DEBIAN_FRONTEND=noninteractive apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y icinga2


# Required packages
# RUN DEBIAN_FRONTEND=noninteractive \
#        apt-get update \
#     && apt-get install -y software-properties-common


# RUN groupadd -g 998 www-data && useradd -u 998 -g 998 www-data

RUN mkdir -p /run/icinga2/cmd
RUN chown icinga.icinga /run/icinga2
RUN chmod 0755 /var/run/icinga2
RUN chown icinga.www-data /run/icinga2/cmd
RUN chmod 2710 /var/run/icinga2/cmd


CMD ["/usr/sbin/icinga2", "daemon"]
