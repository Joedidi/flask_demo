#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: Jamin Chen
@date:  2019/8/19 17:03
@explain: 
@file: Member.py
"""
from flask import Blueprint,request,redirect,jsonify
from common.libs.Helper import ops_render,iPagination
from application import app,db
from common.models.model import Member,PayOrder
from common.libs.UrlManager import UrlManager
from common.libs.Helper import getCurrentDate

route_member= Blueprint('member_page',__name__)

@route_member.route('/index')
def login():
    resp_data = {}
    req = request.values
    page = int(req['p']) if ('p' in req and req['p']) else 1
    query = Member.query
    # app.logger.info(request.values)

    if 'mix_kw' in req:
        query = query.filter(Member.nickname.ilike("%{0}%".format(req['mix_kw'])))

    if 'status' in req and int(req['status']) > -1:
        query = query.filter(Member.status == int(req['status']))

    page_params = {
        'total': query.count(),
        'page_size': app.config['PAGE_SIZE'],
        'page': page,
        'display': app.config['PAGE_DISPLAY'],
        'url': request.full_path.replace('&p={}'.format(page), '')
    }

    pages = iPagination(page_params)
    offset = (page - 1) * app.config['PAGE_SIZE']
    limit = app.config['PAGE_SIZE'] * page
    list = query.order_by(Member.id.desc()).all()[offset:limit]
    resp_data['list'] = list
    resp_data['pages'] = pages
    resp_data['search_con'] = req
    resp_data['status_mapping'] = app.config['STATUS_MAPPING']


    return  ops_render('member/index.html',resp_data)


@route_member.route('/comment')
def comment():
    return ops_render('member/comment.html')


@route_member.route('/info')
def info():
    resp_data = {}
    req = request.args
    id = int(req.get('id', 0))
    app.logger.info(req)
    reback_url = UrlManager.buildUrl("/member/index")
    if id < 1:
        return redirect(reback_url)
    info = Member.query.filter_by(id=id).first()
    if not info:
        return redirect(reback_url)

    order_list = PayOrder.query.filter_by(member_id=id).order_by(PayOrder.id.desc()).limit(10).all()
    resp_data['info'] = info
    resp_data['order_list'] = order_list
    app.logger.info(order_list)
    return ops_render('member/info.html',resp_data)


@route_member.route('/set',methods=["GET","POST"])
def set():
    if request.method=='GET':
        resp_data = {}
        req = request.args
        id = int(req.get('id', 0))
        reback_url = UrlManager.buildUrl("/member/index")
        if id<1:
            return redirect(reback_url)
        info = Member.query.filter_by(id=id).first()
        if not info:
            return redirect(reback_url)
        resp_data['info'] = info
        return ops_render('member/set.html',resp_data)
    resp = {'code': 200, 'msg': '操作成功~~', 'data': {}}
    req = request.values
    id = req['id'] if 'id' in req else 0
    print(req)
    nickname = req['nickname'] if 'nickname' in req else None
    if nickname is None or len(nickname) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入正确的昵称~~"
        return jsonify(resp)

    member_info = Member.query.filter_by(id=id).first()
    if not member_info:
        resp['code'] = -1
        resp['msg'] = "指定会员不存在~~"
        return jsonify(resp)

    member_info.nickname = nickname
    member_info.updated_time = getCurrentDate()
    db.session.add(member_info)
    db.session.commit()
    return jsonify(resp)