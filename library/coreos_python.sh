#!/bin/bash

set -e

changed=false
URL="https://bitbucket.org/pypy/pypy/downloads/pypy2-v6.0.0-linux64.tar.bz2"


# Download
if [[ ! -e /opt/pypy/bin/pypy ]]; then
    mkdir -p /opt/pypy
    wget -O - $URL | tar -xjf - --strip-components=1 -C /opt/pypy
    changed=true
fi

# Binary symlink
if [[ ! -e /opt/bin/python ]]; then
    mkdir -p /opt/bin
    ln -snf /opt/pypy/bin/pypy /opt/bin/python
    changed=true
fi

# Library symlink
if ! test -e /opt/pypy/bin/libtinfo.so.5 ; then
    ln -snf $(ls /usr/lib64/* | grep "libncurses.so.[0-9]\+.\?[0-9]\?" | tail -1) /opt/pypy/bin/libtinfo.so.5
    changed=true
fi


if [ "$changed" = true ] ; then
    echo '{"changed": true}'
else
    echo '{"changed": false}'
fi
exit 0