$(function () {
    $("#reset-pwd-submit").on('click',function(){
        var old_password = $("#old_password").val();
        var new_password = $("#new_password").val();
        var repeat_password = $("#repeat_password").val();
        if(old_password === '' || old_password === null){
            new GHAlert({
                content: '原密码不能为空！',
                type: "fail",
                time: 2000
            }).show();
        }else if(new_password === '' || new_password === null){
            new GHAlert({
                content: '新密码不能为空！',
                type: "fail",
                time: 2000
            }).show();
        }else if(new_password.length <8){
            new GHAlert({
                content: '新密码的长度不能少于8位！',
                type: "fail",
                time: 2000
            }).show();
            $("#new_password").val('');
        }else if(repeat_password === '' || repeat_password === null){
            new GHAlert({
                content: '确认密码不能为空！',
                type: "fail",
                time: 2000
            }).show();
        }else if(new_password !== repeat_password){
            new GHAlert({
                content: '两次密码输入不一致！',
                type: "fail",
                time: 2000
            }).show();
        }else{
            $.ajax({
                url: '/reset_pwd',
                type: 'post',
                dataType: 'json',
                contentType: 'application/json',
                data: JSON.stringify({
                    'action': 'reset_pwd',
                    'old_password':old_password,
                    'new_password':new_password,
                    'repeat_password':repeat_password
                }),
                success: function (res) {
                    if (res.success === 1) {
                        new GHAlert({
                            content: '密码修改成功！',
                            type: "success",
                            time: 2000
                        }).show();
                        $("#old_password").val('');
                        $("#new_password").val('');
                        $("#repeat_password").val('');
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