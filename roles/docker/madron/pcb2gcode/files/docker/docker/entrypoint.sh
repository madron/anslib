#!/bin/bash
set -e

if [[ "$1" = "bash" ]]; then
    exec "$@"
elif [[ "$1" = "millproject" ]]; then
    echo ${*:2}
    /docker/millproject.py ${*:2}
else
    cd /data
    /usr/bin/pcb2gcode $@
fi
