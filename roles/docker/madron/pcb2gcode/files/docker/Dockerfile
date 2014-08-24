FROM ubuntu:trusty
MAINTAINER Massimiliano Ravelli, m.ravelli@mastervoice.it

# docker build -t madron/pcb2gcode roles/docker/madron/pcb2gcode/files/docker/

# Example
# docker run -i -t --rm -v `pwd`:/data  madron/pcb2gcode --help

# Required packages
RUN DEBIAN_FRONTEND=noninteractive apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y pcb2gcode

# Config
ADD docker /docker/
RUN chmod 755 /docker/entrypoint.sh

VOLUME ["/data"]

ENTRYPOINT ["/docker/entrypoint.sh"]
