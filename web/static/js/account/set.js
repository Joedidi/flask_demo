;
var account_set_ops = {
    init: function () {
        this.eventBind();
    },
    eventBind: function () {
        $(".wrap_account_set .save").click(function () {
            var btn_target = $(this);
            if (btn_target.hasClass("disabled")) {
                common_ops.alert("正在处理!!请不要重复提交~~");
                return;
            }
            var id_target = $(".wrap_account_set input[name=id]");
            var id = id_target.val();

            var nickname_target = $(".wrap_account_set input[name=nickname]");
            var nickname = nickname_target.val();

            var email_target = $(".wrap_account_set input[name=email]");
            var email = email_target.val();

            var mobile_target = $(".wrap_account_set input[name=mobile]");
            var mobile = mobile_target.val();

            var login_name_target = $(".wrap_account_set input[name=login_name]");
            var login_name = login_name_target.val();

            var login_pwd_target = $(".wrap_account_set input[name=login_pwd]");
            var login_pwd = login_pwd_target.val();

            if (!nickname || nickname.length < 2) {
                common_ops.tip("请输入符合规范的姓名~~", nickname_target);
                return false;
            }
            if (!mobile || mobile.length < 5) {
                common_ops.tip("请输入符合规范的电话~~", mobile_target);
                return false;
            }
            if (!login_name || login_name.length < 2) {
                common_ops.tip("请输入符合规范的登录名~~", login_name_target);
                return false;
            }
            if (!login_pwd || login_pwd.length < 2) {
                common_ops.tip("请输入符合规范的登录密码~~", login_pwd_target);
                return false;
            }
            if (!email || email.length < 2) {
                common_ops.tip("请输入符合规范的邮箱~~", email_target);
                return false;
            }

            btn_target.addClass("disabled");

            var data = {
                id:id,
                nickname: nickname,
                email: email,
                mobile:mobile,
                login_name:login_name,
                login_pwd:login_pwd
            };

            $.ajax({
                url: common_ops.buildUrl("/account/set"),
                type: 'POST',
                data: data,
                dataType: 'json',
                success: function (res) {
                    btn_target.removeClass("disabled");
                    var callback = null;
                    if (res.code == 200) {
                        callback = function () {
                            window.location.href = window.location.href;
                        }
                    }
                    common_ops.alert(res.msg, callback);
                }
            });


        });
    }
};

$(document).ready(function () {
    account_set_ops.init();
});