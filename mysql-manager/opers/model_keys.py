#!/usr/bin/env python
# coding=utf-8

import simplejson


class DbBase(object):

    _keys = []

    def for_json(self, args):
        if len(args) == 1:
            data = [dict(zip(self._keys, list(args[0])))]
        else:
            data = []
            for arg in args:
                _dict = dict(zip(self._keys, list(arg)))
                data.append(_dict)
            simplejson.dumps(data, for_json=True)
        return data


class ServerModel(DbBase):
    _keys = ['id', 'hostname', 'ip', 'cpu', 'memory', 'ssh_user', 'ssh_password', 'disk', 'desc', 'status', 'created_at']


class MysqlModel(DbBase):
    _keys = ['id', 'uuid',  'idc', 'host_ip', 'name', 'port', 'version', 'status', 'error_msg', 'created_at', 'updated_at']


class BackuphistoryModel(DbBase):
    _keys = ['id', 'uuid', 'mysql_id', 'status', 'start_time', 'finish_time', 'last_time', 'backup_size', 'err_msg']


class TaskModel(DbBase):
    _keys = ['id', 'uuid', 'mysql_id', 'type', 'status', 'params', 'created_at']

