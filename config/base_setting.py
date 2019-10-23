#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: Jamin Chen
@date:  2019/8/16 16:02
@explain: 
@file: base_setting.py
"""

SERVER_PORT = 5000
DEBUG = True
SQLALCHEMY_ECHO = False
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost/food'
SQLALCHEMY_POOL_SIZE=60
SQLALCHEMY_MAX_OVERFLOW=20
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ENCODING = 'utf-8'

JSON_AS_ASCII=False
AUTH_COOKIE_NAME='chenjiaming'


##过滤url
IGNORE_URLS = [
    "^/user/login",
    "^/api",
]

IGNORE_CHECK_LOGIN_URLS = [
    "^/static",
    "^/favicon.ico"
]


PAGE_SIZE = 50
PAGE_DISPLAY = 10


STATUS_MAPPING = {
    "1":"正常",
    "0":"已删除"
}

MINA_APP={
    'appid':'wx639359beb9a015e7',
    'appkey':'4ed7e7bd063239dd6c0237ac64176e8b',
    'paykey':'None',##测试号没有
    'mch_id':'None',##测试号没有
    'callback_url':'/api/order/callback'
}



UPLOAD={
    'ext':['jpg','gif','bmp','jpeg','png'],
    'prefix_path':'/web/static/upload/',
    'prefix_url':'/static/upload/'
}

APP = {
    'domain':'http://192.168.31.78:5000'
}


API_IGNORE_URLS={
    "^/api"
}


PAY_STATUS_MAPPING = {
    "1":"已支付",
    "-8":"待支付",
    "0":"已关闭"
}

PAY_STATUS_DISPLAY_MAPPING = {
    "0":"订单关闭",
    "1":"支付成功",
    "-8":"待支付",
    "-7":"待发货",
    "-6":"待确认",
    "-5":"待评价"
}