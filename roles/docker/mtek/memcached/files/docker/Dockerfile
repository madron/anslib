FROM ubuntu:precise
MAINTAINER Massimiliano Ravelli, m.ravelli@mastervoice.it


# memcache user and group
RUN groupadd -g 999 memcache && useradd -d /nonexistent -u 999 -g 999 memcache


# Required packages
RUN DEBIAN_FRONTEND=noninteractive \
       apt-get update \
    && apt-get install -y memcached



EXPOSE 11211

CMD ["/usr/bin/memcached", "-m", "64", "-p", "11211", "-u", "memcache", "-l", "0.0.0.0"]
