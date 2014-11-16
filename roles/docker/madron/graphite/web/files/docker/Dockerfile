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
#RUN pip install pycairo

# Config
ADD docker /docker/
RUN chmod 755 /docker/entrypoint.sh

ADD auth_admin.json /opt/graphite/webapp/graphite/account/fixtures/
ADD graphite_wsgi.py /opt/graphite/webapp/graphite/graphite_wsgi.py
#ADD settings.py /opt/graphite/webapp/graphite/settings.py
ADD local_settings.py /opt/graphite/webapp/graphite/local_settings.py
ADD logger.py /opt/graphite/webapp/graphite/logger.py


WORKDIR /opt/graphite/webapp/graphite

VOLUME ["/sqlite"]
EXPOSE 80

ENTRYPOINT ["/docker/entrypoint.sh"]
CMD ["gunicorn"]
