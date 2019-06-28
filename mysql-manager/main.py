#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging.config

import tornado.ioloop
import tornado.web

from tornado import httpserver
from routes import handlers
from utils import config
from tasks.tasks import scheduler


class Application(tornado.web.Application):

    def __init__(self):
        settings = dict(
            templates_path=os.path.join(os.path.dirname(__file__), 'templates'),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
        )
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == "__main__":
    http_server = httpserver.HTTPServer(Application())
    logging.config.fileConfig(os.path.join(config.base_dir, r'config/logging.conf'))

    http_server.listen(int(config.PORT))
    # @TODO:需要启动前添加任务
    scheduler.start()
    tornado.ioloop.IOLoop.instance().start()
