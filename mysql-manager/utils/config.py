# -*- coding: utf-8 -*-

import os
import configparser

dirname = os.path.dirname
base_dir = os.path.abspath(dirname(dirname(__file__)))
conf = configparser.RawConfigParser()
current_dir = os.path.dirname(os.path.abspath(__file__))
client_conf_path = os.path.join(os.path.dirname(current_dir), r'config/server.conf')
conf.read(client_conf_path)

PORT = conf.get('server', 'port')

db_plugin = conf.get('db', 'db_plugin')
DB_HOST = conf.get('db', 'database_host_ip')
DB_PORT = int(conf.get('db', 'database_host_port'))
DB_USER = conf.get('db', 'database_user_admin')
DB_PASSED = conf.get('db', 'database_user_admin_passwd')
DB_NAME = conf.get('db', 'database_name')
MINCACHED = int(conf.get('db', 'mincached'))
MAXCACHED = int(conf.get('db', 'maxcached'))
MAXCONN = int(conf.get('db', 'maxconn'))
