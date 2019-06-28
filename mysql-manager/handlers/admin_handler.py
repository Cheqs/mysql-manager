import logging
import traceback
from db.db_mysql import DBAction
from .base_handler import BaseHandler
from tornado.web import asynchronous
from tornado.gen import coroutine
from tornado.concurrent import run_on_executor
from opers.admin_opers import AdminOpers
from concurrent.futures import ThreadPoolExecutor


class LoginHandler(BaseHandler):

    executor = ThreadPoolExecutor(5)

    @asynchronous
    @coroutine
    def post(self):
        try:
            self.body = self.get_request_body()
            logging.info('login, body:%s' % self.body)
            self.conn = DBAction()
            self.admin_oper =  AdminOpers(self.conn)
            ret = yield self.do()
            code, records, msg = 200, [ret], 'successful'
            self.finish(self.result(records, msg, code))
        except:
            error_msg = str(traceback.format_exc())
            print(error_msg)
            code, records, msg = 200, [], 'failed, error:%s' % error_msg
            self.finish(self.result(records , msg, code))

    @run_on_executor
    def do(self):
        return self.admin_oper.login(self.body)


class RegisteHandler(BaseHandler):

    executor = ThreadPoolExecutor(5)

    @asynchronous
    @coroutine
    def post(self):
        try:
            self.body = self.get_request_body()
            logging.info('registe account, body:%s' % self.body)
            self.conn = DBAction()
            self.admin_oper = AdminOpers(self.conn)
            ret = yield self.do()
            code, records, msg = 200, [ret], 'successful'
            self.finish(self.result(records, msg, code))
        except:
            error_msg = str(traceback.format_exc())
            print(error_msg)
            code, records, msg = 200, [], 'failed, error:%s' % error_msg
            self.finish(self.result(records, msg, code))

    @run_on_executor
    def do(self):
        self.admin_oper.registe(self.body)