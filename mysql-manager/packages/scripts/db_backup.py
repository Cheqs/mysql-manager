# -*- coding: UTF-8 -*-
# !/usr/bin/python
# ===============================
# Filename: daily_full_mysqlDateBackup.py
# Description: backup mysql files,base percona xtrabackup
# ===============================
import datetime
import subprocess
import os
import sys
import logging
import re
import argparse
from sys import argv

parser = argparse.ArgumentParser()
parser.add_argument("--port", help="the port of mysql server needs backup", type=int)
parser.add_argument("--file", help="the my.cnf of mysql")
parser.add_argument("--type", help="backup type", type=int)
args = parser.parse_args()

if args.port:
    back_port = args.port
else:
    back_port = 3306

if args.file:
    my_cnf = args.file
else:
    my_cnf = '/etc/my.cnf'

if args.type:
    backup_type = args.type
else:
    backup_type = 1

# logging配置
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s %(levelname)s %(message)s',
                    datefmt='%a,%d %b %Y %H:%M:%S',
                    filename='/dbbackup/logs/backup.log',
                    filemode='a')

# 基本配置
backhost = 'localhost'
backuser = 'root'
backpass = 'Lpx41JL1YqTANPg7'
basedir = '/dbbackup/backup_data'
socketfile = '/tmp/mysql%s.sock' % back_port
tomorrowdate = datetime.date.fromordinal(datetime.date.today().toordinal() + 1).strftime("%y%m%d")
todaydate = datetime.datetime.now().strftime("%y%m%d")
yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%y%m%d")
fullback_dir = '%s/%s-%s' % (basedir, todaydate, back_port)
yesterday_dir = '%s/%s-%s' % (basedir, yesterday, back_port)
stores = '/dbbackup/backup_data_hist'


# 转储旧备份
def storebefore():
    suffix = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y%m%d")
    storedir = "%s/%s-bak" % (stores, suffix)
    if not os.path.exists(storedir):
        os.makedirs(storedir)
        logging.info("%s 文件夹已创建" % storedir)
    else:
        logging.info("%s 文件夹存在" % storedir)
    command = "mv %s  %s" % (yesterday_dir, storedir)
    try:
        subprocess.call(command, shell=True)
    except:
        pass

# 删除7天以前的备份
def cleanstore():
    command = "find %s -type d -mtime +7 |xargs rm -fr" % stores
    subprocess.call(command, shell=True)


# 每天全备
def backupfull():
    commandfull = "innobackupex --defaults-file=%s --host=%s --user=%s --password=%s --socket=%s --no-timestamp \
    --slave-info %s" % (my_cnf, backhost, backuser, backpass, socketfile, fullback_dir)
    start_timestamp = datetime.datetime.now()
    print(commandfull)
    start_time = start_timestamp.strftime("%Y-%m-%d %H:%M:%S")
    logging.info("开始备份: %s" % start_time)
    p = subprocess.Popen(commandfull, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = p.communicate()
    response = {}
    if stderr[-14:-1] == 'completed OK!':
        finish_timestamp = datetime.datetime.now()
        finish_time = finish_timestamp.strftime("%Y-%m-%d %H:%M:%S")
        last_time = (finish_timestamp - start_timestamp).seconds
        backup_size = str(sum(
            sum(os.path.getsize(os.path.join(parent, file)) for file in files) for parent, dirs, files in
            os.walk(basedir)) / 1024 / 1024)
        logging.info("备份完成: %s 备份耗时: %s 备份大小: %s" % (finish_time, last_time, backup_size))
        response['msg'] = "success"
        response['start_time'] = start_time
        response['finish_time'] = finish_time
        response['last_time'] = last_time
        response['backup_size'] = backup_size
    else:
        logging.info("备份失败！")
        response['msg'] = "Faild"
        response['start_time'] = start_time
        response['finish_time'] = '-'
        response['last_time'] = '-'
        response['backup_size'] = '0'

    print(response)


if __name__ == '__main__':
    #storebefore()
    cleanstore()
    backupfull()
    sys.exit(0)
