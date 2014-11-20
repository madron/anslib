#!/bin/bash

/docker/entrypoint.sh backup --overwrite
mkdir -p /backup/source
mkdir -p /backup/destination
mv /backup/base.tar.gz /backup/source/
rdiff-backup --print-statistics /backup/source /backup/destination
echo "Size of postgres data directory in MB: "
du -sm /data
