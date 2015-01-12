FROM ubuntu:trusty
MAINTAINER Massimiliano Ravelli, m.ravelli@mastervoice.it


# User
RUN groupadd -g 999 nagios && useradd -u 999 -g 999 nagios


# Required packages
RUN DEBIAN_FRONTEND=noninteractive apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y wget git openjdk-7-jre
RUN    mkdir /build \
    && cd /build \
    && wget http://aphyr.com/riemann/riemann-0.2.6.tar.bz2.md5 \
    && wget http://aphyr.com/riemann/riemann-0.2.6.tar.bz2 \
    && md5sum -c riemann-0.2.6.tar.bz2.md5 \
    && tar xfj riemann-0.2.6.tar.bz2 \
    && mv /build/riemann-0.2.6 /riemann


EXPOSE 5555 5556

# Configuration
ADD docker/riemann.config /riemann/etc/riemann.config

# VOLUME ["/run/riemann2/cmd"]

CMD ["/riemann/bin/riemann", "-a"]
