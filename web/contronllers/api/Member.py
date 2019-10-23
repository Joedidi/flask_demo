#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: Jamin Chen
@date:  2019/8/26 13:07
@explain: 
@file: Member.py
"""

from web.contronllers.api import route_api
from flask import jsonify, request
from application import app, db
import requests, json
from common.models.model import Member, OauthMemberBind
from common.libs.Helper import getCurrentDate
from common.libs.member.MemberService import MemberService

@route_api.route('/member/login', methods=['GET', 'POST'])
def login():
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    req = request.values
    code = req['code'] if 'code' in req else ''
    if not code or len(code) < 1:
        resp['code'] = -1
        resp['msg'] = '需要code'
        return jsonify(resp)

    openid = MemberService.getWeChatOpenId(code)
    if not openid:
        resp['code'] = -1
        resp['msg'] = '微信出错了~~'
        return jsonify(resp)

    nickname = req['nickName'] if 'nickName' in req else ''
    sex = req['gender'] if 'gender' in req else 0
    avatar = req['avatarUrl'] if 'avatarUrl' in req else ''

    """
    判断是否注册过
    """
    bind_info = OauthMemberBind.query.filter_by(openid=openid, type=1).first()
    if not bind_info:
        model_member = Member()
        model_member.nickname = nickname
        model_member.sex = sex
        model_member.avatar = avatar
        model_member.salt = MemberService.geneSalt()
        model_member.updated_time = model_member.created_time = getCurrentDate()
        db.session.add(model_member)
        db.session.commit()

        model_bind = OauthMemberBind()
        model_bind.member_id = model_member.id
        model_bind.type = 1
        model_bind.openid = openid
        model_bind.extra = ''
        model_bind.updated_time = model_bind.created_time = getCurrentDate()
        db.session.add(model_bind)
        db.session.commit()

        bind_info = model_bind

    member_info = Member.query.filter_by(id=bind_info.member_id).first()
    token = "%s#%s" % (MemberService.geneAuthCode(member_info), member_info.id)
    resp['data'] = {'nickname': nickname}
    return jsonify(resp)



@route_api.route('/member/check-reg',methods=['POST','GET'])
def checkReg():
    resp={'code':200,'msg':'操作成功~','data':{}}
    req = request.values
    code = req['code'] if 'code' in req else ''
    if not code or len(code) < 1:
        resp['code'] = -1
        resp['msg'] = '需要code'
        return jsonify(resp)

    openid = MemberService.getWeChatOpenId(code)
    if not openid:
        resp['code'] = -1
        resp['msg'] = '微信出错了~~'
        return jsonify(resp)

    bind_info = OauthMemberBind.query.filter_by(openid=openid,type=1).first()
    if not bind_info:
        resp['code'] = -1
        resp['msg'] = '未绑定~~'
        return jsonify(resp)

    member_info =Member.query.filter_by(id = bind_info.member_id).first()
    if not member_info:
        resp['code'] = -1
        resp['msg'] = '未查到绑定信息~~'
        return jsonify(resp)

    token = "%s#%s"%(MemberService.geneAuthCode( member_info),member_info.id)
    resp['data']={'token':token}
    return jsonify(resp)