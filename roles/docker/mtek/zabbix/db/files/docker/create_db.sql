CREATE USER zabbix WITH ENCRYPTED PASSWORD 'zabbix' ;
CREATE DATABASE zabbix WITH OWNER zabbix ;
\c zabbix;
SET ROLE zabbix;

