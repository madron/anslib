CREATE USER zabbix WITH ENCRYPTED PASSWORD 'zabbix' ;
CREATE DATABASE zabbix WITH OWNER zabbix ;
SET ROLE zabbix;

\c zabbix;
