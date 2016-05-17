#!/bin/sh

# {{ ansible_managed}}

# platform: {{ arduino_platform }}
# version: {{ arduino_version }}

set -e

cd /opt
tar -x -f /var/lib/ansible/arduino/{{ file_name }}
rm -rf arduino
mv arduino-{{ arduino_version }} arduino

cd /opt/arduino
/bin/sh install.sh
