
$(function(){

    $("form input:not('#submit')").focus(function() {
        $(this).parent().find('span.icon-font').css({"color": "#56afe1", "opacity": '1'});
        $("#login_tip").css("display", "none");
    }).blur(function() {
        $(this).parent().find('span.icon-font').css({"color": "", "opacity": '0.5'});
    });

    //登录方式选择样式
    $("div#nav a:first").click(function() {
        $(this).css("color", "#65c17a");
        $("div#nav a:last").css("color", "#333");
        $(".hidden").css("display", "none");
        $('#childuser').val('');
    });
    $("div#nav a:last").click(function() {
        $(this).css("color", "#65c17a");
        $("div#nav a:first").css("color", "#333");
        $(".hidden").css("display", "block");
    });

    var reg = /^([a-zA-Z0-9]|[._]){1,18}$/;

    //提交登录信息
    $('#submit').click(function(){
        $("#login_tip").css("display", "none");
        $("#error").css("display", "none");
        var username = $("#username").val();
        var childuser = $("#childuser").val();
        var password = $("#password").val();
        if(username == "" || username == null) {
            $("#login_tip").css("display", "block").find('span').html('邮箱账号不能为空！请重新输入');
            return false;
        }
        else if($(".hidden").css("display") == "block") {
            if(childuser == "" || childuser == null || (!reg.test(childuser))) {
                $("#login_tip").css("display", "block").find('span').html('子账号不能为空！');
                return false;
            }
            else if(password == "" || password == null){
                $("#login_tip").css("display", "block").find('span').html('账号或密码错误');
                return false;
            }
            else{
                var password =password;
                return true;
            }
        }
        else if(password == "" || password == null){
            $("#login_tip").css("display", "block").find('span').html('密码输入不能为空！请重新输入');
            return false;
        }
        else {
            var password =password;
            return true;
        }
    });
});