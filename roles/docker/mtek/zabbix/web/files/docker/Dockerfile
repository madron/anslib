FROM ubuntu:trusty
MAINTAINER Massimiliano Ravelli, m.ravelli@mastervoice.it


RUN DEBIAN_FRONTEND=noninteractive \
       apt-get update \
    && apt-get install -y php5 php5-pgsql php5-gd


RUN DEBIAN_FRONTEND=noninteractive \
       apt-get install -y curl \
    && mkdir /build \
    && cd /build \
    && curl -L http://sourceforge.net/projects/zabbix/files/ZABBIX%20Latest%20Stable/2.4.0/zabbix-2.4.0.tar.gz/download | tar xz \
    && mkdir /www \
    && cp -a /build/zabbix-2.4.0/frontends/php/* /www/ \
    && rm -rf /build \
    && apt-get -y --purge remove curl \
    && apt-get -y --purge autoremove

ADD php.ini /etc/php5/apache2/
ADD 000-default.conf /etc/apache2/sites-available/
ADD zabbix.conf.php /www/conf/


EXPOSE 80

ENV APACHE_RUN_USER www-data
ENV APACHE_RUN_GROUP www-data
CMD ["/usr/sbin/apache2ctl", "-D", "FOREGROUND"]
