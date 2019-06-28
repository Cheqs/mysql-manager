# -*- coding: utf-8 -*-

import logging
import traceback

from utils import sql
from utils import common
from utils import constant
from utils.common import do_in_thread, create_process
from opers.model_keys import MysqlModel
from opers.ansible_opers import AnsibleTask, AnsibleHost


class MysqlOpers(MysqlModel):

    def __init__(self, conn):
        self.conn = conn

    def _install(self, ssh_user, ssh_password, cmd):
        try:
            now = common.timestamp()
            self.conn.execute(sql.UPDATE_MYSQL_STATUS, (constant.BUILDING, now, '', self.uuid))
            task = AnsibleTask([AnsibleHost(self.host_ip, 22, 'ssh', ssh_user, ssh_password)])
            logging.info('run cmd:%s on server:%s' % (cmd, self.host_ip))
            code, result = task.exec_shell(cmd)
            if code:
                self.conn.execute(sql.UPDATE_MYSQL_STATUS, (constant.FAILED, now, str(result), self.uuid))
                error_msg = 'update code failed~, cmd:%s\n%s' % (cmd, str(result))
                logging.error(error_msg)
            else:
                self.conn.execute(sql.UPDATE_MYSQL_STATUS, (constant.RUNING, now, '', self.uuid))
        except:
            now = common.timestamp()
            err_msg = str(traceback.format_exc())
            logging.error('run %s error:%s' % (cmd, err_msg))
            self.conn.execute(sql.UPDATE_MYSQL_STATUS, (constant.FAILED, now, err_msg, self.uuid))

    def _stop(self, uuid, host_ip, ssh_user, ssh_password, cmd):
        try:
            now = common.timestamp()
            self.conn.execute(sql.UPDATE_MYSQL_STATUS, (constant.STOPPING, now, '', uuid))
            task = AnsibleTask([AnsibleHost(host_ip, 22, 'ssh', ssh_user, ssh_password)])
            logging.info('run cmd:%s on server:%s' % (cmd, host_ip))
            code, result = task.exec_shell(cmd)
            if code:
                self.conn.execute(sql.UPDATE_MYSQL_STATUS, (constant.FAILED, now, str(result), uuid))
                error_msg = 'update code failed~, cmd:%s\n%s' % (cmd, str(result))
                logging.error(error_msg)
            else:
                self.conn.execute(sql.UPDATE_MYSQL_STATUS, (constant.STOPPED, now, '', uuid))
        except:
            now = common.timestamp()
            err_msg = str(traceback.format_exc())
            logging.error('run %s error:%s' % (cmd, err_msg))
            self.conn.execute(sql.UPDATE_MYSQL_STATUS, (constant.FAILED, now, err_msg, uuid))

    def _restart(self, uuid, host_ip, ssh_user, ssh_password, cmd):
        try:
            now = common.timestamp()
            self.conn.execute(sql.UPDATE_MYSQL_STATUS, (constant.RESTARTING, now, '', uuid))
            task = AnsibleTask([AnsibleHost(host_ip, 22, 'ssh', ssh_user, ssh_password)])
            logging.info('run cmd:%s on server:%s' % (cmd, host_ip))
            code, result = task.exec_shell(cmd)
            if code:
                self.conn.execute(sql.UPDATE_MYSQL_STATUS, (constant.FAILED, now, str(result), uuid))
                error_msg = 'update code failed~, cmd:%s\n%s' % (cmd, str(result))
                logging.error(error_msg)
            else:
                self.conn.execute(sql.UPDATE_MYSQL_STATUS, (constant.RUNING, now, '', uuid))
        except:
            now = common.timestamp()
            err_msg = str(traceback.format_exc())
            logging.error('run %s error:%s' % (cmd, err_msg))
            self.conn.execute(sql.UPDATE_MYSQL_STATUS, (constant.FAILED, now, err_msg, uuid))

    def _start(self, uuid, host_ip, ssh_user, ssh_password, cmd):
        try:
            now = common.timestamp()
            self.conn.execute(sql.UPDATE_MYSQL_STATUS, (constant.STARTING, now, '', uuid))
            task = AnsibleTask([AnsibleHost(host_ip, 22, 'ssh', ssh_user, ssh_password)])
            logging.info('run cmd:%s on server:%s' % (cmd, host_ip))
            code, result = task.exec_shell(cmd)
            if code:
                self.conn.execute(sql.UPDATE_MYSQL_STATUS, (constant.FAILED, now, str(result), uuid))
                error_msg = 'update code failed~, cmd:%s\n%s' % (cmd, str(result))
                logging.error(error_msg)
            else:
                self.conn.execute(sql.UPDATE_MYSQL_STATUS, (constant.RUNING, now, '', uuid))
        except:
            now = common.timestamp()
            err_msg = str(traceback.format_exc())
            logging.error('run %s error:%s' % (cmd, err_msg))
            self.conn.execute(sql.UPDATE_MYSQL_STATUS, (constant.FAILED, now, err_msg, uuid))

    def _backup(self, uuid, host_ip, ssh_user, ssh_password, cmd):
        try:
            now = common.timestamp()
            task = AnsibleTask([AnsibleHost(host_ip, 22, 'ssh', ssh_user, ssh_password)])
            logging.info('run cmd:%s on server:%s' % (cmd, host_ip))
            task_id = common.gen_uuid()
            self.conn.execute(sql.INSERT_BACKUP, (task_id, uuid, constant.BACKUPING, now, '-', '0', '0', '-'))
            code, result = task.exec_shell(cmd)
            back_dict = eval(result['stdout'])

            if back_dict['msg'] == 'success':
                self.conn.execute(sql.UPDATE_BACKUP, (back_dict['msg'], back_dict['start_time'], back_dict['finish_time'], int(back_dict['last_time']), back_dict['backup_size'], back_dict['msg'], task_id))
                logging.info('backup successful')
            else:
                self.conn.execute(sql.UPDATE_BACKUP, ('备份失败',
                                                      back_dict['start_time'],
                                                      back_dict['finish_time'],
                                                      int(back_dict['last_time']),
                                                      int(back_dict['backup_size']),
                                                      back_dict['msg'], task_id))
                error_msg = 'update code failed~, cmd:%s\n%s' % (cmd, str(result))
                logging.error(error_msg)
        except:
            now = common.timestamp()
            err_msg = str(traceback.format_exc())
            logging.error('run %s error:%s' % (cmd, err_msg))
            self.conn.execute(sql.UPDATE_MYSQL_STATUS, (constant.FAILED, now, err_msg, uuid))

    def _record(self):
        now = common.timestamp()
        args = (self.uuid, self.idc, self.host_ip, self.mysql_name, self.mysql_port, self.version, constant.INIT, '', now, now)
        self.conn.execute(sql.INSERT_MYSQL, args)
        logging.info('insert mysql info: %s, %s' % (sql.INSERT_MYSQL, str(args)))

    def _gen_property(self, params):
        self.uuid = common.gen_uuid()
        self.host_ip = params.get('ip')
        self.version = params.get('version')
        self.mysql_port = params.get('port')
        self.mysql_name = params.get('name')
        self.idc = params.get('idc')
        self.adminuser = params.get('adminuser')
        self.adminpass = params.get('adminpass')
        self.ibp_mem = params.get('ibp_mem')

    def _get_ssh(self):
        _sql = sql.SEARCH_HOST % self.host_ip
        ret = self.conn.select(_sql)
        ssh_user = ret[0][5]
        ssh_password = common.decrypt(ret[0][6])
        return ssh_user, ssh_password

    def install_container(self, params):
        self._gen_property(params)
        self._record()
        logging.info('install mysql container')
        # do_in_thread(self._install, constant.INSTALL_MYSQL_BY_SCRIPT_CMD)
        cmd = constant.INSTALL_MYSQL_CONTAINER_CMD % (self.mysql_name, self.mysql_port)
        code, result = create_process(cmd)
        now = common.timestamp()
        if code:
            self.conn.execute(sql.UPDATE_MYSQL_STATUS, (constant.FAILED, now, str(result), self.uuid))
            error_msg = 'update code failed~, cmd:%s\n%s' % (cmd, str(result))
            logging.error(error_msg)
        else:
            self.conn.execute(sql.UPDATE_MYSQL_STATUS, (constant.SUCCESSFUL, now, '', self.uuid))
        return [self.uuid], constant.SUCCESSFUL, 200

    def install(self, params):
        self._gen_property(params)
        self._record()
        logging.info('install mysql')
        ssh_user, ssh_password = self._get_ssh()
        cmd = ('%s %s %s %s %s %s') % (constant.INSTALL_MYSQL_BY_SCRIPT_CMD, str(self.mysql_port), self.ibp_mem, self.version, self.adminuser, self.adminpass)
        do_in_thread(self._install, ssh_user, ssh_password, cmd)
        return [self.uuid], constant.SUCCESSFUL, 200

    def list(self, params={}):
        ret = self.conn.select(sql.LIST_MYSQL)
        return self.for_json(ret)

    def search(self, params={}):
        _sql = sql.SEARCH_MYSQL
        if params.get('host_ip'):
            host_ip = params.get('host_ip').decode('utf-8')
            _sql += ' WHERE host_ip="%s"' % host_ip
        if params.get('mysql_name'):
            mysql_name = params.get('mysql_name').decode('utf-8')
            if 'WHERE' in _sql:
                _sql += ' AND name="%s"' % mysql_name
            else:
                _sql += ' WHERE name="%s"' % mysql_name

        _sql += ' ORDER BY id DESC;'
        print(_sql)
        ret = self.conn.select(_sql)
        return self.for_json(ret)

    def start(self, uuid):
        logging.info("start mysql uuid:%s" % uuid)
        _sql = sql.SEARCH_MYSQL_BY_HOST % uuid
        ret = self.conn.select(_sql)
        host_ip = ret[0][0]
        mysql_port = ret[0][1]
        ssh_user = ret[0][2]
        ssh_password = common.decrypt(ret[0][3])
        cmd = constant.START_MYSQL_BY_PORT % mysql_port

        do_in_thread(self._start, uuid, host_ip, ssh_user, ssh_password, cmd)

    def stop(self, uuid):
        logging.info("stop mysql uuid:%s" % uuid)
        _sql = sql.SEARCH_MYSQL_BY_HOST % uuid
        ret = self.conn.select(_sql)
        host_ip = ret[0][0]
        mysql_port = ret[0][1]
        ssh_user = ret[0][2]
        ssh_password = common.decrypt(ret[0][3])
        cmd = constant.STOP_MYSQL_BY_PORT % mysql_port

        do_in_thread(self._stop, uuid, host_ip, ssh_user, ssh_password, cmd)

    def restart(self, uuid):
        logging.info("stop mysql uuid:%s" % uuid)
        _sql = sql.SEARCH_MYSQL_BY_HOST % uuid
        ret = self.conn.select(_sql)
        host_ip = ret[0][0]
        mysql_port = ret[0][1]
        ssh_user = ret[0][2]
        ssh_password = common.decrypt(ret[0][3])
        cmd = constant.RESTART_MYSQL_BY_PORT % mysql_port

        do_in_thread(self._restart, uuid, host_ip, ssh_user, ssh_password, cmd)

    def delete(self, uuid):
        logging.info("delete mysql uuid:%s" % uuid)
        self.conn.execute(sql.DELETE_MYSQL % uuid)

    def backup(self, uuid):
        #uuid为mysql实例id
        logging.info("backup mysql uuid:%s" % uuid)
        _sql = sql.SEARCH_MYSQL_BY_HOST % uuid
        ret = self.conn.select(_sql)
        host_ip = ret[0][0]
        mysql_port = ret[0][1]
        ssh_user = ret[0][2]
        ssh_password = common.decrypt(ret[0][3])
        cmd = constant.BACKUP_MYSQL_BY_PORT % mysql_port

        do_in_thread(self._backup, uuid, host_ip, ssh_user, ssh_password, cmd)
