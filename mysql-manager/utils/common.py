# -*- coding: utf-8 -*-

import logging
import traceback
import time
import uuid
import threading
import subprocess
import json

import requests
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex

SECRET_KEY = 'keyskeyskeyskeys'
KEY = SECRET_KEY.encode('utf-8')


class FuncThread(threading.Thread):
    def __init__(self, func, *params, **paramMap):
        threading.Thread.__init__(self)
        self.func = func
        self.params = params
        self.paramMap = paramMap
        self.rst = None
        self.finished = False

    def run(self):
        self.rst = self.func(*self.params, **self.paramMap)
        self.finished = True

    def get_result(self):
        return self.rst

    def is_finished(self):
        return self.finished


def do_in_thread(func, *params, **kwargs):
    ft = FuncThread(func, *params, **kwargs)
    ft.start()
    return ft


def create_process(cmd):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    result = p.stdout.read()
    status = p.wait()
    return status, result


def timestamp(style='%Y-%m-%d %H:%M:%S'):
    return time.strftime(style, time.localtime())


def gen_uuid():
    return uuid.uuid1().__str__()


def encrypt(text):
    text = text.encode('utf-8')
    cryptor = AES.new(KEY, AES.MODE_CBC, b'0000000000000000')
    length = 16
    count = len(text)
    if count < length:
        add = (length - count)
        # \0 backspace
        # text = text + ('\0' * add)
        text = text + ('\0' * add).encode('utf-8')
    elif count > length:
        add = (length - (count % length))
        # text = text + ('\0' * add)
        text = text + ('\0' * add).encode('utf-8')
    ciphertext = cryptor.encrypt(text)
    return b2a_hex(ciphertext)


def decrypt(text):
    text = text.encode('utf-8')
    cryptor = AES.new(KEY, AES.MODE_CBC, b'0000000000000000')
    plain_text = cryptor.decrypt(a2b_hex(text))
    return bytes.decode(plain_text).rstrip('\0')


def dohttprequest(url, params):
    if params and not isinstance(params, dict):
        params = eval(params)
    params = json.dumps(params)

    try:
        result = requests.post(url, params)
        logging.info('请求接口，返回信息:%s' % result)

        if result.status_code == 200:

            return 'S', result.text
        else:
            return
    except:
        err_msg = str(traceback.format_exc())
        logging.error('接口请求失败:%s' % err_msg)
