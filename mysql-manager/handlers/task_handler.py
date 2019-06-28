import logging
import traceback
from db.db_mysql import DBAction
from .base_handler import BaseHandler
from tornado.web import asynchronous
from tornado.gen import coroutine
from tornado.concurrent import run_on_executor
from opers.task_opers import TaskOpers
from concurrent.futures import ThreadPoolExecutor


class TaskRegisteHandler(BaseHandler):
    executor = ThreadPoolExecutor(5)

    @asynchronous
    @coroutine
    def post(self):
        try:
            self.body = self.get_request_body()
            logging.info('registe task, body:%s' % self.body)
            self.conn = DBAction()
            self.task_oper = TaskOpers(self.conn)
            yield self.do()
            code, records, msg = 200, [], 'successful'
            self.finish(self.result(records, msg, code))
        except:
            error_msg = str(traceback.format_exc())
            print(error_msg)
            code, records, msg = 200, [], 'failed, error:%s' % error_msg
            self.finish(self.result(records, msg, code))

    @run_on_executor
    def do(self):
        self.task_oper.registe(self.body)


class TaskStartHandler(BaseHandler):
    executor = ThreadPoolExecutor(5)

    @asynchronous
    @coroutine
    def post(self):
        try:
            self.body = self.get_request_body()
            uuid = self.body.get('uuid')
            logging.info('start task, body:%s' % self.body)
            self.conn = DBAction()
            self.task_oper = TaskOpers(self.conn)
            yield self.do(uuid)
            code, records, msg = 200, [], 'successful'
            self.finish(self.result(records, msg, code))
        except:
            error_msg = str(traceback.format_exc())
            print(error_msg)
            code, records, msg = 200, [], 'failed, error:%s' % error_msg
            self.finish(self.result(records, msg, code))

    @run_on_executor
    def do(self, uuid):
        self.task_oper.start(uuid)


class TaskStopHandler(BaseHandler):
    executor = ThreadPoolExecutor(5)

    @asynchronous
    @coroutine
    def post(self):
        try:
            self.body = self.get_request_body()
            uuid = self.body.get('uuid')
            logging.info('stop task, body:%s' % self.body)
            self.conn = DBAction()
            self.task_oper = TaskOpers(self.conn)
            yield self.do(uuid)
            code, records, msg = 200, [], 'successful'
            self.finish(self.result(records, msg, code))
        except:
            error_msg = str(traceback.format_exc())
            print(error_msg)
            code, records, msg = 200, [], 'failed, error:%s' % error_msg
            self.finish(self.result(records, msg, code))

    @run_on_executor
    def do(self, uuid):
        self.task_oper.stop(uuid)


class TaskDeleteHandler(BaseHandler):
    executor = ThreadPoolExecutor(5)

    @asynchronous
    @coroutine
    def post(self):
        try:
            self.body = self.get_request_body()
            uuid = self.body.get('uuid')
            logging.info('delete task, body:%s' % self.body)
            self.conn = DBAction()
            self.task_oper = TaskOpers(self.conn)
            yield self.do(uuid)
            code, records, msg = 200, [], 'successful'
            self.finish(self.result(records, msg, code))
        except:
            error_msg = str(traceback.format_exc())
            code, records, msg = 200, [], 'failed, error:%s' % error_msg
            self.finish(self.result(records, msg, code))

    @run_on_executor
    def do(self, uuid):
        self.task_oper.delete(uuid)


class TaskListHandler(BaseHandler):
    executor = ThreadPoolExecutor(5)

    @asynchronous
    @coroutine
    def get(self):
        try:
            self.conn = DBAction()
            self.task_oper = TaskOpers(self.conn)
            ret = yield self.do()
            logging.info('ret:%s' % ret)
            records, code, msg = ret, 200, 'successful'
            self.finish(self.result(records, msg, code))
        except:
            error_msg = str(traceback.format_exc())
            print(error_msg)
            code, records, msg = 200, ret, 'failed, error:%s' % error_msg
            self.finish(self.result(records, msg, code))

    @run_on_executor
    def do(self):
        return self.task_oper.list()
