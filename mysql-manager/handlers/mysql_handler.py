import logging
import traceback
from .base_handler import BaseHandler
from tornado.web import asynchronous
from tornado.gen import coroutine
from tornado.concurrent import run_on_executor
from opers.mysql_opers import MysqlOpers
from concurrent.futures import ThreadPoolExecutor
from db.db_mysql import DBAction


class MysqlInstallHandler(BaseHandler):
    executor = ThreadPoolExecutor(5)

    @asynchronous
    @coroutine
    def post(self):
        try:
            self.body = self.get_request_body()
            self.conn = DBAction()
            self.mysql_oper = MysqlOpers(self.conn)
            ret = yield self.do()
            code, records, msg = 200, [ret], 'successful'
            self.finish(self.result(records, msg, code))
        except:
            error_msg = str(traceback.format_exc())
            logging.error(error_msg)
            code, records, msg = 200, [], 'failed, error:%s' % error_msg
            self.finish(self.result(records, msg, code))

    @run_on_executor
    def do(self):
        return self.mysql_oper.install(self.body)


class MysqlContainerInstallHandler(BaseHandler):
    executor = ThreadPoolExecutor(5)

    @asynchronous
    @coroutine
    def post(self):
        try:
            self.body = self.get_request_body()
            self.conn = DBAction()
            self.mysql_oper = MysqlOpers(self.conn)
            ret = yield self.do()
            code, records, msg = 200, [ret], 'successful'
            self.finish(self.result(records, msg, code))
        except:
            error_msg = str(traceback.format_exc())
            logging.error(error_msg)
            code, records, msg = 200, [], 'failed, error:%s' % error_msg
            self.finish(self.result(records, msg, code))

    @run_on_executor
    def do(self):
        return self.mysql_oper.install_container(self.body)


class MysqlSearchHandler(BaseHandler):
    executor = ThreadPoolExecutor(5)

    @asynchronous
    @coroutine
    def get(self):
        try:
            self.params = self.get_params()
            print(self.params)

            self.conn = DBAction()
            self.mysql_oper = MysqlOpers(self.conn)
            ret = yield self.do()
            logging.info('ret:%s' % ret)
            records, code, msg = ret, 200, 'successful'
            self.finish(self.result(records, msg, code))
        except:
            error_msg = str(traceback.format_exc())
            logging.error(error_msg)
            records, code, msg = ret, 200, 'failed, error:%s' % error_msg
            self.finish(self.result(records, msg, code))

    @run_on_executor
    def do(self):
        return self.mysql_oper.search(self.params)


class MysqlListHandler(BaseHandler):
    executor = ThreadPoolExecutor(5)

    @asynchronous
    @coroutine
    def get(self):
        try:
            self.conn = DBAction()
            self.mysql_oper = MysqlOpers(self.conn)
            ret = yield self.do()
            logging.info('ret:%s' % ret)
            records, code, msg = ret, 200, 'successful'
            self.finish(self.result(records, msg, code))
        except:
            error_msg = str(traceback.format_exc())
            logging.error(error_msg)
            records, code, msg = ret, 200, 'failed, error:%s' % error_msg
            self.finish(self.result(records, msg, code))

    @run_on_executor
    def do(self):
        return self.mysql_oper.list()


class MysqlStartHandler(BaseHandler):
    executor = ThreadPoolExecutor(5)

    @asynchronous
    @coroutine
    def post(self):
        try:
            self.body = self.get_request_body()
            uuid = self.body.get('uuid')
            self.conn = DBAction()
            self.mysql_oper = MysqlOpers(self.conn)
            yield self.do(uuid)
            code, records, msg = 200, [uuid], 'successful'
            self.finish(self.result(records, msg, code))
        except:
            error_msg = str(traceback.format_exc())
            logging.error(error_msg)
            code, records, msg = 200, [uuid], 'failed, error:%s' % error_msg
            self.finish(self.result(records, msg, code))

    @run_on_executor
    def do(self, uuid):
        self.mysql_oper.start(uuid)


class MysqlStopHandler(BaseHandler):
    executor = ThreadPoolExecutor(5)

    @asynchronous
    @coroutine
    def post(self):
        try:
            self.body = self.get_request_body()
            uuid = self.body.get('uuid')
            self.conn = DBAction()
            self.mysql_oper = MysqlOpers(self.conn)
            yield self.do(uuid)
            code, records, msg = 200, [uuid], 'successful'
            self.finish(self.result(records, msg, code))
        except:
            error_msg = str(traceback.format_exc())
            logging.error(error_msg)
            code, records, msg = 200, [uuid], 'failed, error:%s' % error_msg
            self.finish(self.result(records, msg, code))

    @run_on_executor
    def do(self, uuid):
        self.mysql_oper.stop(uuid)


class MysqlRestartHandler(BaseHandler):
    executor = ThreadPoolExecutor(5)

    @asynchronous
    @coroutine
    def post(self):
        try:
            self.body = self.get_request_body()
            uuid = self.body.get('uuid')
            self.conn = DBAction()
            self.mysql_oper = MysqlOpers(self.conn)
            yield self.do(uuid)
            code, records, msg = 200, [uuid], 'successful'
            self.finish(self.result(records, msg, code))
        except:
            error_msg = str(traceback.format_exc())
            logging.error(error_msg)
            code, records, msg = 200, [uuid], 'failed, error:%s' % error_msg
            self.finish(self.result(records, msg, code))

    @run_on_executor
    def do(self, uuid):
        self.mysql_oper.restart(uuid)


class MysqlDeleteHandler(BaseHandler):
    executor = ThreadPoolExecutor(5)

    @asynchronous
    @coroutine
    def post(self):
        try:
            self.body = self.get_request_body()
            uuid = self.body.get('uuid')
            self.conn = DBAction()
            self.mysql_oper = MysqlOpers(self.conn)
            yield self.do(uuid)
            code, records, msg = 200, [uuid], 'successful'
            self.finish(self.result(records, msg, code))
        except:
            error_msg = str(traceback.format_exc())
            logging.error(error_msg)
            code, records, msg = 200, [uuid], 'failed, error:%s' % error_msg
            self.finish(self.result(records, msg, code))

    @run_on_executor
    def do(self, uuid):
        self.mysql_oper.delete(uuid)


class MysqlBackupHandler(BaseHandler):
    executor = ThreadPoolExecutor(5)

    @asynchronous
    @coroutine
    def post(self):
        try:
            self.body = self.get_request_body()
            uuid = self.body.get('uuid')
            self.conn = DBAction()
            self.mysql_oper = MysqlOpers(self.conn)
            yield self.do(uuid)
            code, records, msg = 200, [uuid], 'successful'
            self.finish(self.result(records, msg, code))
        except:
            error_msg = str(traceback.format_exc())
            logging.error(error_msg)
            code, records, msg = 200, [uuid], 'failed, error:%s' % error_msg
            self.finish(self.result(records, msg, code))

    @run_on_executor
    def do(self, uuid):
        self.mysql_oper.backup(uuid)
