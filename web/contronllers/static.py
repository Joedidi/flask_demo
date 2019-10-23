#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: Jamin Chen
@date:  2019/8/19 13:30
@explain: 
@file: static.py
"""
from flask import Blueprint,send_from_directory
from application import app
route_static = Blueprint('static', __name__)

@route_static.route("/<path:filename>")
def index( filename ):
    return send_from_directory(  app.root_path + "/web/static/" ,filename )