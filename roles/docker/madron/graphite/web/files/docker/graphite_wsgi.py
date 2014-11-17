import os, sys
sys.path.append('/opt/graphite/webapp')

from graphite.wsgi import application

from graphite.logger import log
log.info("graphite.wsgi - pid %d - reloading search index" % os.getpid())

import graphite.metrics.search
