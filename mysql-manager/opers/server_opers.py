# -*- coding: utf-8 -*-

import logging
import traceback
from utils import common
from utils import sql
from opers.model_keys import ServerModel


class ServerOpers(ServerModel):

    def __init__(self, conn):
        self.conn = conn

    def registe(self, params):
        hostname = params.get('hostname')
        ip = params.get('ip')
        cpu = params.get('cpu')
        memory = params.get('memory')
        disk = params.get('disk')
        ssh_user = params.get('ssh_user')
        ssh_password = common.encrypt(params.get('ssh_password'))
        desc = params.get('desc')
        now = common.timestamp()
        logging.info('registe mysql, ip :%s, hostname:%s, cpu:%s, memory:%s' % (ip, hostname, cpu, memory))
        args = (hostname, ip, cpu, memory, disk, ssh_user, ssh_password, "运行中", desc, now)
        try:
            self.conn.execute(sql.INSERT_SERVER, args)
        except:
            err_msg = str(traceback.format_exc())
            logging.error('添加服务器失败，错误信息:%s' % err_msg)

    def list(self):
        ret = self.conn.select(sql.LIST_SERVER)
        return self.for_json(ret)

    def delete(self, ip):
        self.conn.execute(sql.DELETE_SERVER % ip)
