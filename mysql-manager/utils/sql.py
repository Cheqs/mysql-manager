#!/usr/bin/env python
# -*- coding: utf-8 -*-


# SERVER
INSERT_SERVER = """INSERT INTO `server`(`hostname`,`ip`,`cpu`,`memory`,`disk`, `ssh_user`, `ssh_password`, `status`,`desc`,`create_at`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"""
LIST_SERVER = """SELECT *  FROM `server` ORDER BY id DESC;"""
DELETE_SERVER = """DELETE FROM `server` WHERE ip="%s";"""
SEARCH_HOST = """SELECT * FROM server WHERE `ip`='%s' LIMIT 1;"""


# MYSQL
INSERT_MYSQL = """INSERT INTO `mysql`(`uuid`, `idc`,`host_ip`,`name`,`port`,`version`,`status`,`error_msg`,`create_at`,`update_at`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"""
UPDATE_MYSQL_STATUS = """UPDATE `mysql` SET `status`=%s, `update_at`=%s, `error_msg`=%s WHERE `uuid`=%s;"""
LIST_MYSQL = """SELECT *  FROM `mysql` ORDER BY id DESC;"""
SEARCH_MYSQL = """SELECT *  FROM `mysql` """
DELETE_MYSQL = """DELETE FROM `mysql` WHERE uuid="%s";"""
SEARCH_MYSQL_BY_HOST = """SELECT `ip`,`port`,`ssh_user`,`ssh_password` FROM `server` INNER JOIN `mysql` ON `server`.`ip`=`mysql`.`host_ip` WHERE `mysql`.`uuid`="%s" LIMIT 1;"""

# TASK
LIST_TASK = """SELECT * FROM `task` ORDER BY id DESC;"""
INSERT_TASK = """INSERT INTO `task`(`uuid`,`mysql_id`,`type`,`status`,`params`,`created_at`) VALUES(%s,%s,%s,%s,%s,%s);"""
SEARCH_MYSQL_UUID = """SELECT `mysql_id`,`params` FROM `task` WHERE `uuid`="%s";"""
UPDATE_TASK = """UPDATE `task` SET `status`=%s WHERE `uuid`=%s"""
GET_TASK_STATUS = """SELECT `status` FROM `task` WHERE `uuid`="%s";"""
DELETE_TASK = """DELETE FROM `task` WHERE uuid="%s";"""

# BACKUP_HISTORY
INSERT_BACKUP = """INSERT INTO `backup_history`(`uuid`,`mysql_id`,`status`,`start_time`,`finish_time`,`last_time`,`backup_size`, `err_msg`) VALUES(%s,%s,%s,%s,%s,%s,%s,%s);"""
UPDATE_BACKUP = """UPDATE `backup_history` SET `status`=%s,`start_time`=%s,`finish_time`=%s,`last_time`=%s,`backup_size`=%s,`err_msg`=%s WHERE `uuid`=%s;"""

# ADMIN
INSERT_ADMIN = """INSERT INTO `admin`(`username`, `password`, `eamil`, `create_at`) VALUES (%s,%s,%s,%s);"""
SELECT_ADMIN = """SELECT *  FROM `admin` WHERE `username`= "%s" AND `password`="%s";"""
