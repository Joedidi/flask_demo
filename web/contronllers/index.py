#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: Jamin Chen
@date:  2019/8/19 13:37
@explain: 
@file: index.py
"""

from flask import Blueprint,render_template,g
route_index = Blueprint('index_page',__name__)

@route_index.route('/')
def index():
    current_user = g.current_user
    return  render_template('index/index.html',current_user=current_user)