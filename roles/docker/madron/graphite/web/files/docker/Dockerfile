FROM ubuntu:trusty
MAINTAINER Massimiliano Ravelli, massimiliano.ravelli@gmail.com


# Required packages
RUN DEBIAN_FRONTEND=noninteractive apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y python-pip
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y python-cairo

RUN pip install gunicorn
RUN pip install https://github.com/graphite-project/graphite-web/tarball/master
RUN pip install django==1.6.5
RUN pip install django-tagging
RUN pip install pytz
RUN pip install pyparsing

# Redirect log files to stdout/stderr
RUN mkdir -p /graphite/log
RUN ln -sf /dev/stdout /graphite/log/info.log
RUN ln -sf /dev/stdout /graphite/log/cache.log
RUN ln -sf /dev/stdout /graphite/log/rendering.log
RUN ln -sf /dev/stdout /graphite/log/metricaccess.log
RUN ln -sf /dev/stderr /graphite/log/exception.log

# Config
ADD docker /docker/
RUN chmod 755 /docker/entrypoint.sh

ADD local_settings.py /opt/graphite/webapp/graphite/local_settings.py
ADD auth_admin.json /opt/graphite/webapp/graphite/account/fixtures/
ADD graphite_wsgi.py /opt/graphite/webapp/graphite/graphite_wsgi.py


WORKDIR /opt/graphite/webapp/graphite

VOLUME ["/sqlite"]
EXPOSE 80

ENTRYPOINT ["/docker/entrypoint.sh"]
CMD ["gunicorn"]
