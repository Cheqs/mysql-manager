#-*- coding: utf-8 -*-

import logging

from utils import sql
from utils import constant
from utils import common
from opers.model_keys import MysqlModel


class AdminOpers(MysqlModel):

    def __init__(self, conn):
        self.conn = conn

    def login(self, params):
        username = params.get('username')
        password = params.get('password')
        logging.info('check login: username:%s' % username)
        result = self.conn.select(sql.SELECT_ADMIN % (username, password))
        if result:
            return [username], constant.SUCCESSFUL, 200
        else:
            return [username], constant.FAILED, 201

    def registe(self, params):
        now = common.timestamp()
        username = params.get('username')
        passwrod = params.get('passwrod')
        email = params.get('email')
        self.conn.excute(sql.INSERT_ADMIN % (username, passwrod, email, now))
        return [username], constant.SUCCESSFUL, 200



