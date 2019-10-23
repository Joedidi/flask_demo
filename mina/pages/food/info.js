//index.js
//获取应用实例
var app = getApp();
var WxParse = require('../../wxParse/wxParse.js');
// var utils = require('../../utils/utils.js')

Page({
    data: {
        autoplay: true,
        interval: 3000,
        duration: 1000,
        swiperCurrent: 0,
        hideShopPopup: true,
        buyNumber: 1,
        buyNumMin: 1,
        buyNumMax: 1,
        canSubmit: false, //  选中时候是否允许加入购物车
        shopCarInfo: {},
        shopType: "addShopCar",//购物类型，加入购物车或立即购买，默认为加入购物车,
        id: 0,
        shopCarNum: 4,
        commentCount: 2
    },
    onLoad: function (e) {
        var that = this;
        that.setData({
            id: e.id
        });
        // that.setData({
        //     "info": {
        //         "id": 1,
        //         "name": "小鸡炖蘑菇",
        //         "summary": '<p>多色可选的马甲</p><p><img src="http://www.timeface.cn/uploads/times/2015/07/071031_f5Viwp.jpg"/></p><p><br/>相当好吃了</p>',
        //         "total_count": 2,
        //         "comment_count": 2,
        //         "stock": 2,
        //         "price": "80.00",
        //         "main_image": "/images/food.jpg",
        //         "pics": ['/images/food.jpg', '/images/food.jpg']
        //     },
        //     buyNumMax: 2,
        //     commentList: [
        //         {
        //             "score": "好评",
        //             "date": "2017-10-11 10:20:00",
        //             "content": "非常好吃，一直在他们加购买",
        //             "user": {
        //                 "avatar_url": "/images/more/logo.png",
        //                 "nick": "angellee 🐰 🐒"
        //             }
        //         },
        //         {
        //             "score": "好评",
        //             "date": "2017-10-11 10:20:00",
        //             "content": "非常好吃，一直在他们加购买",
        //             "user": {
        //                 "avatar_url": "/images/more/logo.png",
        //                 "nick": "angellee 🐰 🐒"
        //             }
        //         }
        //     ]
        //
        // });
    },
    onShow: function () {
        this.getInfo();

    },

    goShopCar: function () {
        wx.reLaunch({
            url: "/pages/cart/index"
        });
    },
    toAddShopCar: function () {
        this.setData({
            shopType: "addShopCar"
        });
        this.bindGuiGeTap();
    },
    tobuy: function () {
        this.setData({
            shopType: "tobuy"
        });
        this.bindGuiGeTap();
    },
    addShopCar: function () {
        var that = this;
        var data = {
            'id': this.data.info.id,
            'number': this.data.buyNumber
        };
        wx.request({
            url: app.buildUrl('/cart/set'),
            header: app.getRequestHeader(),
            method: 'POST',
            data: data,
            success(res) {
                var resp = res.data;

                app.alert({'content': resp.msg});
                that.setData({
                    hideShopPopup: true,

                });
                that.onShow();
            }
        });

    },
    buyNow: function () {
        var data = {
            goods: [{
                'id': this.data.info.id,
                'number': this.data.buyNumber,
                'price': this.data.info.price
            }]
        };
        wx.navigateTo({
            url: "/pages/order/index?data=" + JSON.stringify(data)
        });
    },
    /**
     * 规格选择弹出框
     */
    bindGuiGeTap: function () {
        this.setData({
            hideShopPopup: false
        })
    }
    ,
    /**
     * 规格选择弹出框隐藏
     */
    closePopupTap: function () {
        this.setData({
            hideShopPopup: true
        })
    }
    ,
    numJianTap: function () {
        if (this.data.buyNumber <= this.data.buyNumMin) {
            return;
        }
        var currentNum = this.data.buyNumber;
        currentNum--;
        this.setData({
            buyNumber: currentNum
        });
    }
    ,
    numJiaTap: function () {
        if (this.data.buyNumber >= this.data.buyNumMax) {
            return;
        }
        var currentNum = this.data.buyNumber;
        currentNum++;
        this.setData({
            buyNumber: currentNum
        });
    }
    ,
//事件处理函数
    swiperchange: function (e) {
        this.setData({
            swiperCurrent: e.detail.current
        })
    }
    ,
    getInfo: function () {
        var that = this;
        wx.request({
            url: app.buildUrl('/food/info'),
            header: app.getRequestHeader(),
            data: {
                id: that.data.id
            },
            success(res) {
                var resp = res.data;
                if (resp.code != 200) {
                    app.alert({'content': resp.msg});
                    wx.navigateTo({
                        url: '/pages/food/index'
                    });
                    return;
                }
                that.setData({
                    info: resp.data.info,
                    buyNumMax: resp.data.info.stock,
                    shopCarNum: resp.data.cart_number
                });
                WxParse.wxParse('article', 'html', resp.data.info.summary, that, 5);

            }
        });

    }
    ,
    onShareAppMessage: function (ops) {
        if (ops.from === 'button') {
            console.log(ops.target)
            console.log(this.data.id)
            console.log(this.data.info)
        }
        var that = this;
        return {
            title: that.data.info.name,
            path: '/pages/food/info?id=' + that.data.info.id,
            success: function (res) {
                // 转发成功
                console.log(res);
                console.log("转发成功:" + JSON.stringify(res));
            },
            fail: function (res) {
                // 转发失败
                console.log("转发失败:" + JSON.stringify(res));

                // success: function (res) {
                //     // 转发成功
                //     console.log('你好')
                //     wx.request({
                //         url: app.buildUrl("/member/share"),
                //         header: app.getRequestHeader(),
                //         method: 'POST',
                //         data: {
                //             url: utils.getCurrentPageUrlWithArgs()
                //         },
                //         success: function (res) {
                //
                //         }
                //     });
                // },
                // fail: function (res) {
                //     // 转发失败
                // }
            }
        }
    }
})
;
