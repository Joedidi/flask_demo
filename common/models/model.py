# coding: utf-8
from sqlalchemy import BigInteger, Column, Date, DateTime, Index, Integer, Numeric, String, Text
from sqlalchemy.schema import FetchedValue
from flask_sqlalchemy import SQLAlchemy
from application import db, app


class AppAccessLog(db.Model):
    __tablename__ = 'app_access_log'

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.BigInteger, nullable=False, index=True, server_default=db.FetchedValue())
    referer_url = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    target_url = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    query_params = db.Column(db.Text, nullable=False)
    ua = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    ip = db.Column(db.String(32), nullable=False, server_default=db.FetchedValue())
    note = db.Column(db.String(1000), nullable=False, server_default=db.FetchedValue())
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())


class AppErrorLog(db.Model):
    __tablename__ = 'app_error_log'

    id = db.Column(db.Integer, primary_key=True)
    referer_url = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    target_url = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    query_params = db.Column(db.Text, nullable=False)
    content = db.Column(db.String, nullable=False)
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())


class Food(db.Model):
    __tablename__ = 'food'

    id = db.Column(db.Integer, primary_key=True)
    cat_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    name = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    price = db.Column(db.Numeric(10, 2), nullable=False, server_default=db.FetchedValue())
    main_image = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    summary = db.Column(db.String(10000), nullable=False, server_default=db.FetchedValue())
    stock = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    tags = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    month_count = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    total_count = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    view_count = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    comment_count = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())


class FoodCat(db.Model):
    __tablename__ = 'food_cat'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(50), nullable=False, server_default=db.FetchedValue())
    weight = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())

    @property
    def status_desc(self):
        return app.config['STATUS_MAPPING'][str(self.status)]

class FoodSaleChangeLog(db.Model):
    __tablename__ = 'food_sale_change_log'

    id = db.Column(db.Integer, primary_key=True)
    food_id = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    quantity = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    price = db.Column(db.Numeric(10, 2), nullable=False, server_default=db.FetchedValue())
    member_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())


class FoodStockChangeLog(db.Model):
    __tablename__ = 'food_stock_change_log'

    id = db.Column(db.Integer, primary_key=True)
    food_id = db.Column(db.Integer, nullable=False, index=True)
    unit = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    total_stock = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    note = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())


class Image(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    file_key = db.Column(db.String(60), nullable=False, server_default=db.FetchedValue())
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())


class Member(db.Model):
    __tablename__ = 'member'

    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    mobile = db.Column(db.String(11), nullable=False, server_default=db.FetchedValue())
    sex = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    avatar = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    salt = db.Column(db.String(32), nullable=False, server_default=db.FetchedValue())
    reg_ip = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())

    @property
    def status_desc(self):
        return app.config['STATUS_MAPPING'][str(self.status)]


    @property
    def sex_desc(self):
        sex_mapping={
            '0':'未知',
            '1':'男',
            '2':'女',
        }
        return sex_mapping[str(self.sex)]


class MemberAddres(db.Model):
    __tablename__ = 'member_address'
    __table_args__ = (
        db.Index('idx_member_id_status', 'member_id', 'status'),
    )

    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    nickname = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue())
    mobile = db.Column(db.String(11), nullable=False, server_default=db.FetchedValue())
    province_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    province_str = db.Column(db.String(50), nullable=False, server_default=db.FetchedValue())
    city_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    city_str = db.Column(db.String(50), nullable=False, server_default=db.FetchedValue())
    area_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    area_str = db.Column(db.String(50), nullable=False, server_default=db.FetchedValue())
    address = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    is_default = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())


class MemberCart(db.Model):
    __tablename__ = 'member_cart'

    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.BigInteger, nullable=False, index=True, server_default=db.FetchedValue())
    food_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    quantity = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())


class MemberComment(db.Model):
    __tablename__ = 'member_comments'

    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    food_ids = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    pay_order_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    score = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    content = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())


class OauthAccessToken(db.Model):
    __tablename__ = 'oauth_access_token'

    id = db.Column(db.Integer, primary_key=True)
    access_token = db.Column(db.String(600), nullable=False, server_default=db.FetchedValue())
    expired_time = db.Column(db.DateTime, nullable=False, index=True, server_default=db.FetchedValue())
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())


class OauthMemberBind(db.Model):
    __tablename__ = 'oauth_member_bind'
    __table_args__ = (
        db.Index('idx_type_openid', 'type', 'openid'),
    )

    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    client_type = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue())
    type = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    openid = db.Column(db.String(80), nullable=False, server_default=db.FetchedValue())
    unionid = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    extra = db.Column(db.Text, nullable=False)
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())


class PayOrder(db.Model):
    __tablename__ = 'pay_order'
    __table_args__ = (
        db.Index('idx_member_id_status', 'member_id', 'status'),
    )

    id = db.Column(db.Integer, primary_key=True)
    order_sn = db.Column(db.String(40), nullable=False, unique=True, server_default=db.FetchedValue())
    member_id = db.Column(db.BigInteger, nullable=False, server_default=db.FetchedValue())
    total_price = db.Column(db.Numeric(10, 2), nullable=False, server_default=db.FetchedValue())
    yun_price = db.Column(db.Numeric(10, 2), nullable=False, server_default=db.FetchedValue())
    pay_price = db.Column(db.Numeric(10, 2), nullable=False, server_default=db.FetchedValue())
    pay_sn = db.Column(db.String(128), nullable=False, server_default=db.FetchedValue())
    prepay_id = db.Column(db.String(128), nullable=False, server_default=db.FetchedValue())
    note = db.Column(db.Text, nullable=False)
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    express_status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    express_address_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    express_info = db.Column(db.String(1000), nullable=False, server_default=db.FetchedValue())
    comment_status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    pay_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())

    @property
    def pay_status(self):
        tmp_status = self.status
        if self.status == 1:
            tmp_status = self.express_status
            if self.express_status == 1 and self.comment_status == 0:
                tmp_status = -5
            if self.express_status == 1 and self.comment_status == 1:
                tmp_status = 1
        return tmp_status

    @property
    def status_desc(self):
        return app.config['PAY_STATUS_DISPLAY_MAPPING'][ str( self.pay_status )]

    @property
    def order_number(self):
        order_number = self.created_time.strftime("%Y%m%d%H%M%S")
        order_number = order_number + str(self.id).zfill(5)
        return order_number

class PayOrderCallbackDatum(db.Model):
    __tablename__ = 'pay_order_callback_data'

    id = db.Column(db.Integer, primary_key=True)
    pay_order_id = db.Column(db.Integer, nullable=False, unique=True, server_default=db.FetchedValue())
    pay_data = db.Column(db.Text, nullable=False)
    refund_data = db.Column(db.Text, nullable=False)
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())


class PayOrderItem(db.Model):
    __tablename__ = 'pay_order_item'

    id = db.Column(db.Integer, primary_key=True)
    pay_order_id = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    member_id = db.Column(db.BigInteger, nullable=False, server_default=db.FetchedValue())
    quantity = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    price = db.Column(db.Numeric(10, 2), nullable=False, server_default=db.FetchedValue())
    food_id = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    note = db.Column(db.Text, nullable=False)
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())


class QueueList(db.Model):
    __tablename__ = 'queue_list'

    id = db.Column(db.Integer, primary_key=True)
    queue_name = db.Column(db.String(30), nullable=False, server_default=db.FetchedValue())
    data = db.Column(db.String(500), nullable=False, server_default=db.FetchedValue())
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())


class StatDailyFood(db.Model):
    __tablename__ = 'stat_daily_food'
    __table_args__ = (
        db.Index('date_food_id', 'date', 'food_id'),
    )

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    food_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    total_count = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    total_pay_money = db.Column(db.Numeric(10, 2), nullable=False, server_default=db.FetchedValue())
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())


class StatDailyMember(db.Model):
    __tablename__ = 'stat_daily_member'
    __table_args__ = (
        db.Index('idx_date_member_id', 'date', 'member_id'),
    )

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    member_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    total_shared_count = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    total_pay_money = db.Column(db.Numeric(10, 2), nullable=False, server_default=db.FetchedValue())
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())


class StatDailySite(db.Model):
    __tablename__ = 'stat_daily_site'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, index=True)
    total_pay_money = db.Column(db.Numeric(10, 2), nullable=False, server_default=db.FetchedValue())
    total_member_count = db.Column(db.Integer, nullable=False)
    total_new_member_count = db.Column(db.Integer, nullable=False)
    total_order_count = db.Column(db.Integer, nullable=False)
    total_shared_count = db.Column(db.Integer, nullable=False)
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())


class User(db.Model):
    __tablename__ = 'user'

    uid = db.Column(db.BigInteger, primary_key=True)
    nickname = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    mobile = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue())
    email = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    sex = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    avatar = db.Column(db.String(64), nullable=False, server_default=db.FetchedValue())
    login_name = db.Column(db.String(20), nullable=False, unique=True, server_default=db.FetchedValue())
    login_pwd = db.Column(db.String(32), nullable=False, server_default=db.FetchedValue())
    login_salt = db.Column(db.String(32), nullable=False, server_default=db.FetchedValue())
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())


class WxShareHistory(db.Model):
    __tablename__ = 'wx_share_history'

    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    share_url = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
