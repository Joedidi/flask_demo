;
var cat_set_ops = {
    init: function () {
        this.eventBind();
    },
    eventBind: function () {
        $(".wrap_cat_set .save").click(function () {
            var btn_target = $(this);
            if (btn_target.hasClass("disabled")) {
                common_ops.alert("正在处理!!请不要重复提交~~");
                return;
            }

            var name_target = $(".wrap_cat_set input[name=name]");
            var name = name_target.val();

            if (!name || name.length < 2) {
                common_ops.tip("请输入符合规范的姓名~~", name_target);
                return false;
            }

            btn_target.addClass("disabled");

            var data = {
                name: name,
                weight: $(".wrap_cat_set input[name=weight]").val(),
                id:$(".wrap_cat_set input[name=id]").val()
            };

            $.ajax({
                url: common_ops.buildUrl("/food/cat-set"),
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
    cat_set_ops.init();
});