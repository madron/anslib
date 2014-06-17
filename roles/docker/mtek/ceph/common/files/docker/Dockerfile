FROM ubuntu:trusty
MAINTAINER Massimiliano Ravelli, m.ravelli@mastervoice.it

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y wget software-properties-common

# Repository
RUN wget -q -O- 'https://ceph.com/git/?p=ceph.git;a=blob_plain;f=keys/release.asc' | sudo apt-key add -
RUN apt-add-repository 'deb http://ceph.com/debian-firefly/ trusty main'
# RUN apt-add-repository 'deb http://ceph.com/packages/ceph-extras/debian trusty main'
RUN apt-get update

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y ceph
