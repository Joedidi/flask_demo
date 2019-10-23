#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: Jamin Chen
@date:  2019/8/27 10:25
@explain: 
@file: MemberService.py
"""
from application import app
import requests, json
import hashlib, base64, random, string


class MemberService():

    @staticmethod
    def geneAuthCode(member_info=None):
        m = hashlib.md5()
        str = "%s-%s-%s" % (member_info.id, member_info.salt, member_info.status)
        m.update(str.encode("utf-8"))
        return m.hexdigest()

    @staticmethod
    def geneSalt(length=16):
        keylist = [random.choice((string.ascii_letters + string.digits)) for i in range(length)]
        return ("".join(keylist))


    @staticmethod
    def getWeChatOpenId(code):
        url = 'https://api.weixin.qq.com/sns/jscode2session?appid={APPID}&secret={SECRET}&js_code={JSCODE}&grant_type=authorization_code'.format(
            APPID=app.config['MINA_APP']['appid'], SECRET=app.config['MINA_APP']['appkey'], JSCODE=code)
        r = requests.get(url)
        res = json.loads(r.text)
        if 'openid' in res:
            openid = res['openid']
        return openid
