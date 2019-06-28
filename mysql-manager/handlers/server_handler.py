import logging
import traceback
from db.db_mysql import DBAction
from .base_handler import BaseHandler
from tornado.web import asynchronous
from tornado.gen import coroutine
from tornado.concurrent import run_on_executor
from opers.server_opers import ServerOpers
from concurrent.futures import ThreadPoolExecutor


class ServerRegisteHandler(BaseHandler):
    executor = ThreadPoolExecutor(5)

    @asynchronous
    @coroutine
    def post(self):
        try:
            self.body = self.get_request_body()
            logging.info('registe server, body:%s' % self.body)
            self.conn = DBAction()
            self.server_oper = ServerOpers(self.conn)
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
        self.server_oper.registe(self.body)


class ServerDeleteHandler(BaseHandler):
    executor = ThreadPoolExecutor(5)

    @asynchronous
    @coroutine
    def post(self):
        try:
            self.body = self.get_request_body()
            self.conn = DBAction()
            self.server_oper = ServerOpers(self.conn)
            yield self.do()
            records, code, msg = [], 200, 'successful'
            self.finish(self.result(records, msg, code))
        except:
            error_msg = str(traceback.format_exc())
            logging.error(error_msg)
            code, records, msg = 200, [], 'failed, error:%s' % error_msg
            self.finish(self.result(records, msg, code))

    @run_on_executor
    def do(self):
        return self.server_oper.delete(self.body.get('ip'))


class ServerListHandler(BaseHandler):
    executor = ThreadPoolExecutor(5)

    @asynchronous
    @coroutine
    def get(self):
        try:
            self.conn = DBAction()
            self.server_oper = ServerOpers(self.conn)
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
        return self.server_oper.list()
