<?php
// Zabbix GUI configuration file
global $DB;

$DB['TYPE']     = 'POSTGRESQL';
$DB['SERVER']   = 'zabbix_server_db';
$DB['PORT']     = '0';
$DB['DATABASE'] = 'zabbix';
$DB['USER']     = 'zabbix';
$DB['PASSWORD'] = 'zabbix';

// SCHEMA is relevant only for IBM_DB2 database
$DB['SCHEMA'] = '';

$ZBX_SERVER      = 'zabbix_server';
$ZBX_SERVER_PORT = '10051';
$ZBX_SERVER_NAME = '';

$IMAGE_FORMAT_DEFAULT = IMAGE_FORMAT_PNG;
?>
