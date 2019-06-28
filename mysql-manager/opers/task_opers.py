# -*- coding: utf-8 -*-

import logging
import traceback

from utils import sql
from utils import common
from utils import constant
from utils.common import do_in_thread, create_process, dohttprequest
from opers.model_keys import TaskModel
from tasks.tasks import scheduler


class TaskOpers(TaskModel):

    def __init__(self, conn):
        self.conn = conn

    def _get_mysql_info(self, uuid):
        _sql = sql.SEARCH_MYSQL_UUID % uuid
        ret = self.conn.select(_sql)
        mysql_uuid = ret[0][0]
        params = ret[0][0]
        return mysql_uuid, params

    def list(self, params={}):
        ret = self.conn.select(sql.LIST_TASK)
        return self.for_json(ret)

    def registe(self, params):
        uuid = common.gen_uuid()
        mysql_id = params.get('mysql_id')
        type = params.get('type')
        params = params.get('params')
        now = common.timestamp()
        logging.info('registe task uuid:%s mysql_id:%s type:%s params:%s' % (uuid, mysql_id, type, params))
        args = (uuid, mysql_id, type, 0, params, now)
        try:
            self.conn.execute(sql.INSERT_TASK, args)
        except:
            err_msg = str(traceback.format_exc())
            logging.error('添加服务器失败，错误信息:%s' % err_msg)

    def start(self, uuid):
        # uuid为传入的task_id
        args = {}
        mysql_id, params = self._get_mysql_info(uuid)
        args['uuid'] = mysql_id
        url = constant.TOKEN + '/mysql/backup'
        # 动态添加备份任务
        scheduler.add_job(dohttprequest, 'interval', seconds=300, id=uuid, args=[url, args])
        self.conn.execute(sql.UPDATE_TASK, (1, uuid))

    def stop(self, uuid):

        try:
            scheduler.remove_job(uuid)
            self.conn.execute(sql.UPDATE_TASK, (0, uuid))
        except:
            err_msg = str(traceback.format_exc())
            logging.error('移除任务: %s 失败，错误信息:%s' % (uuid, err_msg))

    def delete(self, uuid):
        # 从task表里删除记录，需要先停止task任务，即状态为0
        ret = self.conn.select(sql.GET_TASK_STATUS % uuid)

        task_status = int(ret[0][0])

        if task_status:
            logging.error('移除任务: %s 失败，需要先停止任务' % (uuid))
        else:
            self.conn.execute(sql.DELETE_TASK % uuid)
