FROM ubuntu:trusty
MAINTAINER Massimiliano Ravelli, m.ravelli@mastervoice.it

# docker build -t madron/pcb2gcode roles/docker/madron/pcb2gcode/files/docker/

# Example
# docker run -d --name gcode-data -v /data busybox true
# docker run -i -t --rm -v /usr/local/bin/docker:/docker -v /var/run/docker.sock:/docker.sock svendowideit/samba gcode-data
# docker run -i -t --rm --volumes-from gcode-data madron/pcb2gcode millproject --base-name testcnc
# docker run -i -t --rm --volumes-from gcode-data madron/pcb2gcode --help

# Links:
# http://sourceforge.net/apps/mediawiki/pcb2gcode
# http://reprap.org/wiki/PCB_Milling#pcb2gcode

# Required packages
RUN DEBIAN_FRONTEND=noninteractive apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y pcb2gcode
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y man
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y python-jinja2


# Config
ADD docker /docker/
RUN chmod 755 /docker/entrypoint.sh

VOLUME ["/data"]

ENTRYPOINT ["/docker/entrypoint.sh"]
