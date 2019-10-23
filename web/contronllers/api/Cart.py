#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: Jamin Chen
@date:  2019/9/6 14:09
@explain: 
@file: Cart.py
"""

from web.contronllers.api import route_api
from flask import request, jsonify, g
from common.models.model import Food, MemberCart
from common.libs.member.CartService import CartService
from common.libs.Helper import selectFilterObj, getDictFilterField
from common.libs.UrlManager import UrlManager
import json
from application import app


@route_api.route('/cart/set', methods=["POST"])
def setCart():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    req = request.values
    food_id = int(req['id']) if 'id' in req else 0
    number = int(req['number']) if 'number' in req else 0
    if food_id < 1 or number < 1:
        resp['code'] = -1
        resp['msg'] = '添加购物车失败-1'
        return jsonify(resp)

    member_info = g.member_info
    if not member_info:
        resp['code'] = -1
        resp['msg'] = '添加购物车失败-2'
        return jsonify(resp)

    food_info = Food.query.filter_by(id=food_id).first()
    if not food_info:
        resp['code'] = -1
        resp['msg'] = '添加购物车失败-3'
        return jsonify(resp)

    if food_info.stock < number:
        resp['code'] = -1
        resp['msg'] = '库存不足'
        return jsonify(resp)

    ret = CartService.setItems(member_id=member_info.id, food_id=food_id, number=number)
    if not ret:
        resp['code'] = -1
        resp['msg'] = '购物车添加失败~~'
        return jsonify(resp)
    resp['data'] = req

    return jsonify(resp)


@route_api.route('/cart/index')
def CartIndex():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    member_info = g.member_info
    if not member_info:
        resp['code'] = -1
        resp['msg'] = '获取失败，未登录~'
        return jsonify(resp)

    cart_list = MemberCart.query.filter_by(member_id=member_info.id).all()
    data_cart_list = []
    if cart_list:
        food_ids = selectFilterObj(cart_list, 'food_id')
        food_map = getDictFilterField(Food, Food.id, 'id', food_ids)
        for item in cart_list:
            tmp_food_info = food_map[item.food_id]
            tmp_data = {
                "id": item.id,
                "number": item.quantity,
                "food_id": item.food_id,
                "name": tmp_food_info.name,
                "price": str(tmp_food_info.price),
                "pic_url": UrlManager.buildImageUrl(tmp_food_info.main_image),
                "active": True
            }
            data_cart_list.append(tmp_data)
        resp['data']['list'] = data_cart_list
    return jsonify(resp)


@route_api.route('/cart/del',methods=["POST"])
def CartDel():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    req = request.values
    goods = req['goods'] if 'goods' in req else None
    if not goods:
        resp['code'] = -1
        resp['msg'] = '购物车删除失败~~-1'
        return jsonify(resp)
    goods=json.loads(goods)
    member_info = g.member_info
    if not member_info:
        resp['code'] = -1
        resp['msg'] = '获取失败，未登录~'
        return jsonify(resp)

    ret = CartService.delItems(member_info.id,goods)
    if not ret:
        resp['code'] = -1
        resp['msg'] = '购物车删除失败~~-2'
        return jsonify(resp)
    return resp
