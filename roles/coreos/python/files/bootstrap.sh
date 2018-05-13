#/bin/bash

set -e

if [[ -e /opt/bin/python ]]; then
  exit 0
fi

URL="https://bitbucket.org/pypy/pypy/downloads/pypy2-v6.0.0-linux64.tar.bz2"

mkdir -p /opt/pypy
wget -O - $URL | tar -xjf - --strip-components=1 -C /opt/pypy

## library fixup
ln -snf /usr/lib64/libncurses.so.5.9 /opt/pypy/bin/libtinfo.so.5

# python symlink
ln -snf /opt/pypy/bin/pypy /opt/bin/python
