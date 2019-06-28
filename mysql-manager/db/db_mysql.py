#!/usr/bin/env python
#coding=utf-8

import logging
import traceback
import pymysql
from DBUtils.PooledDB import PooledDB
from utils import config


db_pool_ins = None

class DBPool():
    def __init__(self, host, port, user, passwd, db):
        self.pool = PooledDB(creator=pymysql, mincached=1, maxcached=50, maxconnections=100, 
                             blocking=True, host=host, port=port, user=user, passwd=passwd, db=db, charset='utf8',)

    def get_connection(self):
        return self.pool.connection()


class DBAction():
    
    def __init__(self, host=config.DB_HOST, port=config.DB_PORT, user=config.DB_USER, passwd=config.DB_PASSED, db=config.DB_NAME):
        #建立和数据库系统的连接
        global db_pool_ins
        if db_pool_ins == None:
            db_pool_ins = DBPool(host, port, user, passwd, db)
        self.conn = db_pool_ins.get_connection()
        #获取操作游标
        self.cursor = self.conn.cursor()

    def close_database(self):
        self.cursor.close()
        self.conn.close()

    def execute(self, sql, params=()):
        '''
        数据的插入，更新，删除
        :param database:
        :param sql:
        :return: 成功：0，失败：1
        '''
        try:
            #执行sql语句
            self.cursor.execute(sql, params)
            #提交到数据库执行
            self.conn.commit()
            return 0
        except:
            logging.error("sql is %s, params is %s error. %s" % (sql, params, traceback.format_exc()))
            self.conn.rollback()
            raise Exception

    def execute_many(self, sql, params=()):
        '''
        数据的插入，更新，删除
        :param sql:
        :param params:
        :return: 成功：0，失败：1
        '''
        #执行sql语句
        self.cursor.executemany(sql, params)
        #提交到数据库执行
        self.conn.commit()

    def execute_count(self, sql, params=()):
        '''
        数据的插入，更新，删除
        :return: 受影响的条数
        '''
        #执行sql语句
        count = self.cursor.execute(sql, params)
        #提交到数据库执行
        self.conn.commit()
        return count

    def select(self, sql, params=()):
        '''
        :param database:
        :param sql:
        :return: ((),(),...,())
        '''
        self.cursor.execute(sql, params)
        result = self.cursor.fetchall()

        return result

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()
