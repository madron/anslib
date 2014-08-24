#!/bin/bash
set -e

if [[ "$1" = "bash" ]]; then
    exec "$@"
else
    cd /data
    /usr/bin/pcb2gcode $@
fi
