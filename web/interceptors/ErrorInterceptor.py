#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: Jamin Chen
@date:  2019/8/23 14:18
@explain: 
@file: ErrorInterceptor.py
"""
from application import app
from common.libs.Helper import ops_render
from common.libs.LogService import LogService

@app.errorhandler(404)
def error_404(e):
    LogService.addErrorLog(str(e))
    return ops_render('error/error.html',{'status':'404','msg':'你访问的不存在'})