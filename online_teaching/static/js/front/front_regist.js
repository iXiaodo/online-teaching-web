$(function () {
    var reg = /^[a-z0-9]+([._\\\\-]*[a-z0-9])*@([a-z0-9]+[-a-z0-9]*[a-z0-9]+.){1,63}[a-z0-9]+$/;
    var is_send = false;
    $("#captcha-btn").click(function () {
        var email = $("#email").val();
        if(email == "" || email == null){
            $("#login_tip").removeClass("hidden");
            $("#login_tip span").html("邮箱帐号输入不能为空！！");
        } else if (!reg.test(email)) {
            $("#login_tip").removeClass("hidden");
            $("#login_tip span").html("邮箱格式输入不正确！！");
        } else {
            $("#login_tip").addClass("hidden");
            var countdown=60;
            function settime() {
                if (countdown == 0) {
                    $("#captcha-btn").removeClass("disabled");
                    countdown = 60;
                    $("#captcha-btn").text("免费获取验证码");
                    return;
                } else {
                    $("#captcha-btn").addClass("disabled", true);
                    $("#captcha-btn").text("重新发送(" + countdown + ")");
                    countdown--;
                }
                setTimeout(function() {
                        settime() }
                    ,1000)
            }
            if(is_send === false){
                settime();
            }else{
                new GHAlert({
                    content: '邮箱验证码发送成功,不能重复发送！',
                    type: "success",
                    time: 3000
                }).show();
            }
            $.ajax({
                url: '/regist',
                type: 'post',
                dataType: 'json',
                contentType: 'application/json',
                data: JSON.stringify({
                    'action': 'send_email',
                    'email':email
                }),
                success: function (res) {
                    if (res.success === 1) {
                        new GHAlert({
                            content: '邮箱验证码发送成功！',
                            type: "success",
                            time: 3000
                        }).show();
                        is_send = true;
                    }
                    else {
                        new GHAlert({
                            content: res.err_msg,
                            type: "fail",
                            time: 3000
                        }).show();
                        is_send = true;
                    }
                }
            });
        }
    });
    $("#submit").click(function (event) {
        event.preventDefault();
        var captcha = $("#captcha").val();
        var password = $("#password").val();
        var email = $("#email").val();
        var reg_captcha = /^[A-Za-z0-9]{4}$/;
        if(email == "" || email == null){
            $("#login_tip").removeClass("hidden");
            $("#login_tip span").html("邮箱帐号输入不能为空！！");
        } else if (!reg.test(email)) {
            $("#login_tip").removeClass("hidden");
            $("#login_tip span").html("邮箱格式输入不正确！！");
        } else if(password == "" || password == null){
            $("#login_tip").removeClass("hidden");
            $("#login_tip span").html("密码输入不能为空！！");
        } else if(password.length <6){
            $("#login_tip").removeClass("hidden");
            $("#login_tip span").html("密码位数至少6位数！！");
        } else if(captcha == "" || captcha== null){
            $("#login_tip").removeClass("hidden");
            $("#login_tip span").html("邮箱验证码不能为空！！");
        } else if(!reg_captcha.test(captcha)){
            $("#login_tip").removeClass("hidden");
            $("#login_tip span").html("邮箱验证码个数只能为4位！！");
        } else{
            $("#login_tip").addClass("hidden");
            $.ajax({
                url: '/regist',
                type: 'post',
                dataType: 'json',
                contentType: 'application/json',
                data: JSON.stringify({
                    'action': 'regist',
                    'email':email,
                    'password':password,
                    'captcha':captcha
                }),
                success: function (res) {
                    if (res.success === 1) {
                        new GHAlert({
                            content: '恭喜您！帐号注册成功！',
                            type: "success",
                            time: 2000
                        }).show();
                        setTimeout(function () {
                            window.location.href = '/signin';
                        },1000)
                    }
                    else {
                        new GHAlert({
                            content: res.err_msg,
                            type: "fail",
                            time: 3000
                        }).show();
                    }
                }
            });
        }
    });
});