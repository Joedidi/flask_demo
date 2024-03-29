#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: Jamin Chen
@date:  2019/8/27 10:25
@explain: 
@file: MemberService.py
"""
from application import app,db
import requests, json
from common.models.model import MemberCart
from common.libs.Helper import getCurrentDate
import hashlib, base64, random, string


class CartService():

    @staticmethod
    def setItems(member_id=0,food_id=0,number = 0):
        if member_id<1 or food_id<1 or number<1:
            return False
        cart_info = MemberCart.query.filter_by(food_id = food_id,member_id=member_id).first()
        if cart_info:
            model_cart = cart_info
        else:
            model_cart = MemberCart()
            model_cart.member_id = member_id
            model_cart.created_time =getCurrentDate()

        model_cart.food_id = food_id
        model_cart.quantity = number
        model_cart.updated_time = getCurrentDate()
        db.session.add(model_cart)
        db.session.commit()
        return True


    @staticmethod
    def delItems(member_id=0,items = None):
        if member_id<1 or not items:
            return False
        for item in items:
            MemberCart.query.filter_by(food_id=item['id'],member_id = member_id).delete()
        db.session.commit()

        return True