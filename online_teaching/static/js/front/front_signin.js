$(function () {
    var reg = /^[a-z0-9]+([._\\\\-]*[a-z0-9])*@([a-z0-9]+[-a-z0-9]*[a-z0-9]+.){1,63}[a-z0-9]+$/;
    $("#submit").click(function () {
        var email = $("#email").val();
        var password = $("#password").val();
        if (email == '' || email == null) {
            var insert_con = '邮箱帐号不能为空！请输入';
            $("#login_tip").removeClass("hidden");
            $("#login_tip span").html(insert_con);
            return
        }
        if (password == '' || password == null) {
            var insert_html = '密码不能为空！请输入';
            $("#login_tip").removeClass("hidden");
            $("#login_tip span").html(insert_html);
            return
        }
        if (!reg.test(email)) {
            $("#login_tip").removeClass("hidden");
            $("#login_tip span").html("邮箱格式输入有误，请重新输入！");
            return
        }
        if (password.length < 6) {
            $("#login_tip").removeClass("hidden");
            $("#login_tip span").html("密码不能少于6位，请重新输入！");
            return
        }
    });
});