#!/usr/bin/env python
# coding=utf-8

SUCCESSFUL = "successful"
FAILED = "failed"

INIT = 'init'
BUILDING = '正在安装...'
RUNING = '正在运行'
STOPPING = '正在停止'
STOPPED = '停止运行'
STARTING = '正在启动...'
RESTARTING = '正在重启...'
BACKUPING = '正在备份...'

INSTALL_MYSQL_BY_SCRIPT_CMD = 'sh /usr/local/src/install_mysql.sh'
INSTALL_MYSQL_CONTAINER_CMD = 'docker run --name %s -p %s:3306 -e MYSQL_ROOT_PASSWORD=pythonclass -d mysql:5.7.21'
STOP_MYSQL_BY_PORT = 'sh /data/mysql/mysql%s/mysql stop'
START_MYSQL_BY_PORT = 'sh /data/mysql/mysql%s/mysql start'
RESTART_MYSQL_BY_PORT = 'sh /data/mysql/mysql%s/mysql restart'
BACKUP_MYSQL_BY_PORT = 'python /usr/local/src/db_backup.py %s'

TOKEN = 'http://127.0.0.1:9123/api/v1'
