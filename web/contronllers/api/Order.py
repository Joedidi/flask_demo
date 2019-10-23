#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: Jamin Chen
@date:  2019/9/9 18:08
@explain: 
@file: Order.py
"""

from web.contronllers.api import route_api
from flask import request, jsonify, g
from common.models.model import Food, MemberCart, PayOrder, OauthMemberBind
from common.libs.pay.payService import PayService
from common.libs.pay.WeChatService import WeChatService
from common.libs.Helper import selectFilterObj, getDictFilterField
from common.libs.UrlManager import UrlManager
from common.libs.member.CartService import CartService
import json, decimal
from application import app, db


@route_api.route('/order/info', methods=["POST"])
def orderInfo():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    req = request.values
    parms_goods = req['goods'] if 'goods' in req else None

    member_info = g.member_info
    if not member_info:
        resp['code'] = -1
        resp['msg'] = '获取失败，未登录~'
        return jsonify(resp)

    if parms_goods:
        parms_goods_list = json.loads(parms_goods)

    food_dic = {}
    for item in parms_goods_list:
        food_dic[item['id']] = item['number']

    food_ids = food_dic.keys()
    app.logger.info(food_ids)
    food_list = Food.query.filter(Food.id.in_(food_ids)).all()
    data_food_list = []
    yun_price = pay_price = decimal.Decimal(0.00)
    if food_list:
        for item in food_list:
            tmp_data = {
                'id': item.id,
                'name': item.name,
                'price': str(item.price),
                'pic_url': UrlManager.buildImageUrl(item.main_image),
                'number': food_dic[item.id],
            }
            data_food_list.append(tmp_data)
            pay_price = pay_price + item.price * int(food_dic[item.id])
    default_address = {
        'name': "编程浪子",
        'mobile': "12345678901",
        'address': "上海市浦东新区XX",
    }
    resp['data']['food_list'] = data_food_list
    resp['data']['pay_price'] = str(pay_price)
    resp['data']['default_address'] = default_address
    resp['data']['total_price'] = str(pay_price + yun_price)
    resp['data']['yun_price'] = str(yun_price)
    return jsonify(resp)


@route_api.route('/order/create', methods=["POST"])
def orderCreate():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    req = request.values
    type = req['type'] if 'type' in req else ''
    parms_goods = req['goods'] if 'goods' in req else None
    member_info = g.member_info
    if not member_info:
        resp['code'] = -1
        resp['msg'] = '获取失败，未登录~'
        return jsonify(resp)
    items = []
    if parms_goods:
        parms_goods_list = json.loads(parms_goods)
    else:
        resp['code'] = -1
        resp['msg'] = '下单失败，没有商品'
        return jsonify(resp)

    member_info = g.member_info
    target = PayService()
    parms = {}
    resp = target.createOrder(member_info.id, parms_goods_list, parms)
    if resp['code'] == 200 and type == 'cart':
        CartService.delItems(member_info.id, items)

    return jsonify(resp)


@route_api.route('/order/pay', methods=["POST"])
def orderPay():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    member_info = g.member_info
    req = request.values
    order_sn = req['order_sn'] if 'order_sn' in req else ''
    pay_order_info = PayOrder.query.filter_by(order_sn=order_sn).first()
    if not pay_order_info:
        resp['code'] = -1
        resp['msg'] = '系统繁忙，稍后再试'
        return jsonify(resp)
    oauth_bind_info = OauthMemberBind.query.filter_by(member_id=member_info.id).first()

    if not oauth_bind_info:
        resp['code'] = -1
        resp['msg'] = '系统繁忙，稍后再试'
        return jsonify(resp)

    config_mina = app.config['MINA_APP']
    notify_url = app.config["APP"]["domain"] + config_mina['callback_url']
    target_wechat = WeChatService(merchant_key=config_mina['paykey'])
    data = {
        'appid': config_mina['appid'],
        'mch_id': config_mina['mch_id'],
        'nonce_str': target_wechat.get_nonce_str(),
        'body': '订餐',  # 商品描述
        'out_trade_no': pay_order_info.order_sn,  # 商户订单号
        'total_fee': int(pay_order_info.total_price * 100),
        'notify_url': notify_url,
        'trade_type': "JSAPI",
        'openid': oauth_bind_info.openid
    }

    pay_info = target_wechat.get_pay_info(data)

    # 保存prepay_id为了后面发模板消息
    pay_order_info.prepay_id = pay_info['prepay_id']
    db.session.add(pay_order_info)
    db.session.commit()

    resp['data']['pay_info'] = pay_info
    return jsonify(resp)


@route_api.route("/order/callback", methods=["POST"])
def orderCallback():
    """
    <xml>
   <appid>wx2421b1c4370ec43b</appid>
   <attach>支付测试</attach>
   <body>JSAPI支付测试</body>
   <mch_id>10000100</mch_id>
   <detail><![CDATA[{ "goods_detail":[ { "goods_id":"iphone6s_16G", "wxpay_goods_id":"1001", "goods_name":"iPhone6s 16G", "quantity":1, "price":528800, "goods_category":"123456", "body":"苹果手机" }, { "goods_id":"iphone6s_32G", "wxpay_goods_id":"1002", "goods_name":"iPhone6s 32G", "quantity":1, "price":608800, "goods_category":"123789", "body":"苹果手机" } ] }]]></detail>
   <nonce_str>1add1a30ac87aa2db72f57a2375d8fec</nonce_str>
   <notify_url>http://wxpay.wxutil.com/pub_v2/pay/notify.v2.php</notify_url>
   <openid>oUpF8uMuAJO_M2pxb1Q9zNjWeS6o</openid>
   <out_trade_no>1415659990</out_trade_no>
   <spbill_create_ip>14.23.150.211</spbill_create_ip>
   <total_fee>1</total_fee>
   <trade_type>JSAPI</trade_type>
   <sign>0CB01533B8C1EF103065174F50BCA001</sign>
</xml>


    :return:
    """


    result_data = {
        'return_code': 'SUCCESS',
        'return_msg': 'OK'
    }
    header = {'Content-Type': 'application/xml'}
    config_mina = app.config['MINA_APP']
    target_wechat = WeChatService(merchant_key=config_mina['paykey'])
    callback_data = target_wechat.xml_to_dict(request.data)
    app.logger.info(callback_data)
    sign = callback_data['sign']
    callback_data.pop('sign')
    gene_sign = target_wechat.create_sign(callback_data)
    app.logger.info(gene_sign)
    if sign != gene_sign:
        result_data['return_code'] = result_data['return_msg'] = 'FAIL'
        return target_wechat.dict_to_xml(result_data), header
    if callback_data['result_code'] != 'SUCCESS':
        result_data['return_code'] = result_data['return_msg'] = 'FAIL'
        return target_wechat.dict_to_xml(result_data), header
    #核对订单号
    order_sn = callback_data['out_trade_no']
    pay_order_info = PayOrder.query.filter_by(order_sn=order_sn).first()
    if not pay_order_info:
        result_data['return_code'] = result_data['return_msg'] = 'FAIL'
        return target_wechat.dict_to_xml(result_data), header
    # 核对金额
    if int(pay_order_info.total_price * 100) != int(callback_data['total_fee']):
        result_data['return_code'] = result_data['return_msg'] = 'FAIL'
        return target_wechat.dict_to_xml(result_data), header
    # 核对状态码
    if pay_order_info.status == 1:
        return target_wechat.dict_to_xml(result_data), header

    target_pay = PayService()
    target_pay.orderSuccess(pay_order_id=pay_order_info.id, params={"pay_sn": callback_data['transaction_id']})
    target_pay.addPayCallbackData(pay_order_id=pay_order_info.id, data=request.data)
    return target_wechat.dict_to_xml(result_data), header
