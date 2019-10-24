#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: Jamin Chen
@date:  2019/8/23 14:54
@explain: 
@file: __init__.py.py
"""
from flask import Blueprint

route_api= Blueprint('api_page',__name__)
from web.contronllers.api.Member import *
from web.contronllers.api.Food import *
from web.contronllers.api.Cart import *
from web.contronllers.api.Order import *
from web.contronllers.api.My import *
from web.contronllers.api.Address import *

@route_api.route('/')
def index():
    return  'Mina api'