FROM nginx
MAINTAINER Massimiliano Ravelli, massimiliano.ravelli@gmail.com


# Required packages
RUN DEBIAN_FRONTEND=noninteractive apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y python-pip
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y python-cairo

RUN pip install https://github.com/graphite-project/graphite-web/tarball/master
RUN pip install django==1.6.5
RUN pip install django-tagging
RUN pip install pytz

RUN echo "SECRET_KEY = 'notsosecret'" >> /opt/graphite/webapp/graphite/local_settings.py
RUN export PYTHONPATH=$PYTHONPATH:/opt/graphite/webapp; cd /opt/graphite/webapp/graphite; django-admin.py collectstatic --noinput  --settings=graphite.settings

ADD default.conf /etc/nginx/conf.d/default.conf
