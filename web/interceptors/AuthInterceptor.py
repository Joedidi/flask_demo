#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: Jamin Chen
@date:  2019/8/20 15:33
@explain: 
@file: AuthInterceptor.py
"""

from application import app
from flask import request,redirect,g
from common.models.model import User
from common.libs.user.UserService import UserService
from common.libs.UrlManager import UrlManager
from common.libs.LogService import LogService
import re


@app.before_request
def before_request():
    ignore_urls = app.config['IGNORE_URLS']
    app.logger.info(ignore_urls)
    ignore_check_login_urls = app.config['IGNORE_CHECK_LOGIN_URLS']
    path = request.path
    # 如果是静态文件就不要查询用户信息了
    pattern = re.compile('%s' % "|".join(ignore_check_login_urls))
    if pattern.match(path):
        return

    if '/api' in path:
        return

    pattern = re.compile('%s' % "|".join(ignore_urls))
    if pattern.match(path):
        return

    user_info = check_login()
    g.current_user = None
    if user_info:
        g.current_user = user_info

    #加入日志
    LogService.addAccesslog()

    if not user_info:
        return redirect(UrlManager.buildUrl("/user/login"))
    return

"""
判断用户是否已经登录
"""
def check_login():
    cookies = request.cookies
    auth_cookie = cookies[app.config['AUTH_COOKIE_NAME']] if app.config['AUTH_COOKIE_NAME'] in cookies else None
    if auth_cookie is None:
        return False

    auth_info = auth_cookie.split('#')
    if len(auth_info) !=2:
        return False
    try:
       user_info = User.query.filter_by(uid = auth_info[1]).first()
    except Exception:
        return False

    if user_info is None:
        return False

    if auth_info[0] != UserService.geneAuthCode(user_info):
        return False

    if user_info.status != 1:
        return False

    return user_info