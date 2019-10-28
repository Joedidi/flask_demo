#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: Jamin Chen
@date:  2019/8/16 16:06
@explain: 
@file: www.py
"""

'''
统一拦截器，提供登录日志功能
'''
from web.interceptors.AuthInterceptor import *
from web.interceptors.ApiAuthInterceptor import *
from web.interceptors.ErrorInterceptor import *

'''
蓝图功能，对所有的url进行蓝图功能配置
'''
from application import app
from web.contronllers.user.User import route_user
from web.contronllers.static import route_static
from web.contronllers.index import route_index
from web.contronllers.account.Account import route_account
from web.contronllers.food.Food import route_food
from web.contronllers.member.Member import route_member
from web.contronllers.finance.Finance import route_finance
from web.contronllers.stat.Stat import route_stat
from web.contronllers.upload.Upload import route_upload
from web.contronllers.api import route_api
from web.contronllers.chart import route_chart


app.register_blueprint(route_user ,url_prefix = '/user')

app.register_blueprint( route_static,url_prefix = "/static" )

app.register_blueprint( route_index,url_prefix = "/" )

app.register_blueprint(route_account ,url_prefix = '/account')

app.register_blueprint(route_food ,url_prefix = '/food')

app.register_blueprint(route_member ,url_prefix = '/member')

app.register_blueprint(route_finance ,url_prefix = '/finance')

app.register_blueprint(route_stat ,url_prefix = '/stat')

app.register_blueprint(route_api ,url_prefix = '/api')

app.register_blueprint(route_upload ,url_prefix = '/upload')


app.register_blueprint(route_chart ,url_prefix = '/chart')


1233133