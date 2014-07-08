FROM ubuntu:trusty
MAINTAINER Massimiliano Ravelli, m.ravelli@mastervoice.it

# Required packages
RUN DEBIAN_FRONTEND=noninteractive apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y git
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y golang

# Download
RUN mkdir -p /gocode/src/github.com/kelseyhightower
RUN git clone https://github.com/kelseyhightower/coreos-ipxe-server.git /gocode/src/github.com/kelseyhightower/coreos-ipxe-server

# Build
RUN cd /gocode/src/github.com/kelseyhightower/coreos-ipxe-server && GOPATH=/gocode/ go build .
RUN cp /gocode/src/github.com/kelseyhightower/coreos-ipxe-server/coreos-ipxe-server /
RUN chmod 755 /coreos-ipxe-server


EXPOSE 4777

VOLUME ["/opt/coreos-ipxe-server"]

CMD /coreos-ipxe-server
