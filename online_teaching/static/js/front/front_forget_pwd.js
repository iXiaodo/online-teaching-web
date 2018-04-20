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
                url: '/forgetpwd',
                type: 'post',
                dataType: 'json',
                contentType: 'application/json',
                data: JSON.stringify({
                    'action': 'retrieve_password',
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
    $("#send-email-btn").click(function () {

        var email = $("#email").val();
        var captcha = $("#captcha").val();
        if(email === ''||email ===null){
            $("#login_tip").removeClass("hidden");
            $("#login_tip span").html("邮箱帐号输入不能为空！！");
        }else if(!reg.test(email)){
            $("#login_tip").removeClass("hidden");
            $("#login_tip span").html("邮箱格式输入不正确！！");
        }else if(captcha === ''|| captcha === null){
            $("#login_tip").removeClass("hidden");
            $("#login_tip span").html("邮箱验证码输入不能为空！！");
        }else{
            $("#login_tip").addClass("hidden");
            $.ajax({
                url: '/forgetpwd',
                type: 'post',
                dataType: 'json',
                contentType: 'application/json',
                data: JSON.stringify({
                    'action': 'verify',
                    'email':email,
                    'captcha':captcha
                }),
                success: function (res) {
                    if (res.success === 1) {
                        is_send = true;
                        $("#update-pwd").attr("data-email",email);
                        $("#update-pwd").modal('show');
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

    //保存修改后的密码
    $("#update-pwd-btn").click(function () {
        var password = $("#password").val(),
            repeat_password = $("#repeat-password").val(),
            email = $("#update-pwd").attr("data-email");
        if (password === '' || password === null){
            new GHAlert({
                content: '密码不能为空！',
                type: "fail",
                time: 3000
            }).show();
        }else if(repeat_password === '' || repeat_password === null){
            new GHAlert({
                content: '确认密码不能为空！',
                type: "fail",
                time: 3000
            }).show();
        }else if(password.length < 8){
            new GHAlert({
                content: '密码长度不能少于8位！',
                type: "fail",
                time: 3000
            }).show();
            $("#password").val('');
        }else if(repeat_password.length < 8){
            new GHAlert({
                content: '确认密码长度不能少于8位！',
                type: "fail",
                time: 3000
            }).show();
            $("#repeat-password").val('');
        }else if(password !== repeat_password){
            new GHAlert({
                content: '两次密码输入不一致！',
                type: "fail",
                time: 3000
            }).show();
        }else if(email === '' || email === null){
            new GHAlert({
                content: '邮箱获取错误！',
                type: "fail",
                time: 3000
            }).show();
        } else{
            $.ajax({
                url: '/forgetpwd',
                type: 'post',
                dataType: 'json',
                contentType: 'application/json',
                data: JSON.stringify({
                    'action': 'save',
                    'email':email,
                    'password':password,
                    'repeat_password':repeat_password
                }),
                success: function (res) {
                    if (res.success === 1) {
                        $("#update-pwd").modal('hide');
                        new GHAlert({
                            content: '密码找回成功！',
                            type: "success",
                            time: 3000
                        }).show();
                        setTimeout(function() {
                            $("#email").val('');
                            $("#captcha").val('');
                            window.location.href = '/signin';
                                 },2000)

                    } else {
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