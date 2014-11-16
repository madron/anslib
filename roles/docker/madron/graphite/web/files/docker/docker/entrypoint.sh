#!/bin/bash
set -e

export PYTHONPATH=$PYTHONPATH:/opt/graphite/webapp

if [[ "$1" = "gunicorn" ]]; then
    cd /opt/graphite/webapp/graphite
    if [ ! -f "/sqlite/graphite.db" ]
    then
        django-admin.py syncdb --noinput --settings=graphite.settings
        django-admin.py loaddata auth_admin --settings=graphite.settings
    fi
    # django-admin.py createsuperuser --username=admin --email=admin@example.com --settings=graphite.settings
    exec gunicorn --log-file=- --bind 0.0.0.0:80 graphite_wsgi:application
else
    exec "$@"
fi
