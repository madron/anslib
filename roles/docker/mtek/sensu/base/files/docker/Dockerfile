FROM ubuntu:trusty
MAINTAINER Massimiliano Ravelli, m.ravelli@mastervoice.it


# Sensu user and group
RUN groupadd \
    --gid  999 \
    sensu \
 && useradd  \
    --uid 999 \
    --gid 999 \
    --comment "Sensu Monitoring Framework" \
    --home-dir /opt/sensu \
    --shell /bin/false \
    sensu


# Sensu repository
RUN DEBIAN_FRONTEND=noninteractive \
       apt-get update \
    && apt-get install -y wget python3-jinja2 \
    && wget -q http://repos.sensuapp.org/apt/pubkey.gpg -O- | sudo apt-key add - \
    && echo "deb     http://repos.sensuapp.org/apt sensu main" > /etc/apt/sources.list.d/sensu.list \
    && apt-get -y --purge remove wget \
    && apt-get -y --purge autoremove \
    && apt-get update
