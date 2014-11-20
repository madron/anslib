#!/bin/bash
set -e

exec sudo -i -u postgres /docker/data.py "$@"
