import os, sys
sys.path.append('/opt/graphite/webapp')
os.environ['DJANGO_SETTINGS_MODULE'] = 'graphite.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()

# READ THIS
# Initializing the search index can be very expensive, please include
# the WSGIImportScript directive pointing to this script in your vhost
# config to ensure the index is preloaded before any requests are handed
# to the process.
from graphite.logger import log
log.info("graphite.wsgi - pid %d - reloading search index" % os.getpid())

# import logging
# import sys

# root = logging.getLogger()
# root.setLevel(logging.DEBUG)

# ch = logging.StreamHandler(sys.stdout)
# ch.setLevel(logging.DEBUG)
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# ch.setFormatter(formatter)
# root.addHandler(ch)

import graphite.metrics.search
