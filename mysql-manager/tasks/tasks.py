# -*- coding: utf-8 -*-#

# -------------------------------------------------------------------------------
# Name:         tasks
# Description:
# Author:       xucl
# Date:         2019-06-26
# -------------------------------------------------------------------------------

from pytz import utc

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

from utils import config

url = 'mysql+pymysql://%s:%s@%s/%s?charset=utf8' % (config.DB_USER, config.DB_PASSED, config.DB_HOST, config.DB_NAME)

jobstores = {
    'default': RedisJobStore()
}
executors = {
    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(5)
}
job_defaults = {
    'coalesce': False,
    'max_instances': 3
}
scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=utc)
