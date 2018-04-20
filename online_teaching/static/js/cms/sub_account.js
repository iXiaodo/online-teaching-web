$(function(){
    //渲染子账户
    function render_subaccout() {
        $.ajax({
            url: '/cms/subaccount',
            cache: false,
            success: function(res){
                if(res.success===1){
                    var data = res.data,
                        insert_html = '';
                    if (!$.isEmptyObject(data)){
                        for(var user in data){
                            if(data[user]['status'] === true) {
                                insert_html += '<li class="list-group-item" data-name="' + data[user]['user_name'] + '">' + data[user]['user_name'] + '<i class="iconfont ban" title="禁用此账户" data-email="' + data[user]['user_email'] + '">&#xe6f2;</i></li>';
                            }else{
                                insert_html += '<li class="list-group-item" data-name="' + data[user]['user_name'] + '">' + data[user]['user_name'] + '<i class="iconfont start-use" title="启用此账户" data-email="' + data[user]['user_email'] + '">&#xe6f2;</i></li>';
                            }
                        }
                         $("#sub-account-list").html(insert_html);
                    }else {
                        $("#add-sub-btn").remove();
                        insert_html = '<li class="list-group-item">很抱歉！您没有查看此页面的权限</li>';
                        $("#sub-account-list").html(insert_html);
                    }
                } else{
                    new GHAlert({
                        content: res['err_msg'],
                        type: "fail",
                        time: 2000
                    }).show();
                }
            }
        });
    }
    render_subaccout();
    //
    //禁用账户
    $("#sub-account-list").on('click','i.iconfont.ban',function () {
        var username = $(this).parent().attr('data-name');
        var email = $(this).attr('data-email');
        if(email === '' || email === null){
            new GHAlert({
                content: '帐号信息有误!',
                type: "fail",
                time: 3000
            }).show();
            return
        }
        zeroModal.confirm({
            content: '确定要禁用账户【'+ username +'】吗？',
            contentDetail: '提交后此账户将会暂停使用!',
            transition: true,
            okFn: function() {
                $.ajax({
                    url: '/cms/subaccount',
                    type: 'post',
                    dataType: 'json',
                    contentType: 'application/json',
                    data: JSON.stringify({
                        'action': 'ban',
                        'email':email,
                    }),
                    success: function (res) {
                        if (res.success === 1) {
                            new GHAlert({
                                content: '禁用成功！',
                                type: "success",
                                time: 2000
                            }).show();
                            render_subaccout();
                        }
                        else {
                            new GHAlert({
                                content: res.err_msg,
                                type: "fail",
                                time: 2000
                            }).show();
                        }
                    }
                })
            },
            cancelFn: function() {}
        });
    });

    //启用账户
    $("#sub-account-list").on('click','i.iconfont.start-use',function () {
        var username = $(this).parent().attr('data-name');
        var email = $(this).attr('data-email');
        if(email === '' || email === null){
            new GHAlert({
                content: '帐号信息有误!',
                type: "fail",
                time: 3000
            }).show();
            return
        }
        zeroModal.confirm({
            content: '确定要启用账户【'+ username +'】吗？',
            contentDetail: '提交后此账户将恢复使用!',
            transition: true,
            okFn: function() {
                $.ajax({
                    url: '/cms/subaccount',
                    type: 'post',
                    dataType: 'json',
                    contentType: 'application/json',
                    data: JSON.stringify({
                        'action': 'start_use',
                        'email':email,
                    }),
                    success: function (res) {
                        if (res.success === 1) {
                            new GHAlert({
                                content: '账户启用成功！',
                                type: "success",
                                time: 2000
                            }).show();
                            render_subaccout();
                        }
                        else {
                            new GHAlert({
                                content: res.err_msg,
                                type: "fail",
                                time: 2000
                            }).show();
                        }
                    }
                })
            },
            cancelFn: function() {}
        });
    });

    //添加账户

    $("#add-sub-btn").on('click',function () {
        $("#add-subaccout-page").removeClass("hidden");


        //渲染角色权限信息
        function render_role_permission() {
            $.ajax({
                url: '/cms/get_rolesPermissions/',
                cache: false,
                success: function(res){
                    if(res.success===1){
                        var data = res.data,
                            insert_html = '';
                        $("#user_email").val('');
                        $("#password").val('');
                        if (!$.isEmptyObject(data)){
                            insert_html += '<select class="form-control" id="permission-select">';
                            for(var i in data['permissions']){
                                insert_html += '<option value="'+ data['permissions'][i] +'">'+ data['permissions'][i] +'</option>';
                            }
                            insert_html += ' </select>';
                            $("#permission").html(insert_html);
                        }else {
                            console.log('error');
                        }
                    } else{
                        new GHAlert({
                            content: res['err_msg'],
                            type: "fail",
                            time: 2000
                        }).show();
                    }
                }
            })
        }
        render_role_permission();

        //保存信息
        var reg_tel =  /^1[3|4|5|7|8][0-9]{9}$/;
        var reg_email = /^([\.a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(\.[a-zA-Z0-9_-])+/;
        $("#save-user").click(function () {
            var username= $("#sub_name").val();
            var tel = $("#tel").val();
            var email = $("#user_email").val();
            var password = $("#password").val();
            var permission = $("#permission-select").val();
            if(username ==='' || username === null){
                new GHAlert({
                    content: '用户名不能为空',
                    type: "fail",
                    time: 2000
                }).show();
            }else if(tel ==='' || tel === null){
                new GHAlert({
                    content: '手机号不能为空',
                    type: "fail",
                    time: 2000
                }).show();
            }else if(!reg_tel.test(tel) ){
                new GHAlert({
                    content: '手机号码格式错误!',
                    type: "fail",
                    time: 2000
                }).show();
            }else if(email === '' || email === null ){
                new GHAlert({
                    content: '邮箱不能为空!',
                    type: "fail",
                    time: 2000
                }).show();
            }else if(!reg_email.test(email) ){
                new GHAlert({
                    content: '邮箱格式错误!',
                    type: "fail",
                    time: 2000
                }).show();
            }else if(password === '' || password ===null ){
                new GHAlert({
                    content: '密码不能为空!',
                    type: "fail",
                    time: 2000
                }).show();
            }else if(password.length <8 ){
                new GHAlert({
                    content: '密码位数不能少于8位!',
                    type: "fail",
                    time: 2000
                }).show();
            }else{
                 $.ajax({
                     url: '/cms/subaccount',
                    type: 'post',
                    dataType: 'json',
                    contentType: 'application/json',
                    data: JSON.stringify({
                        'action': 'add',
                        'email':email,
                        'username':username,
                        'password':password,
                        'permission':permission,
                        'tel':tel
                    }),
                    success: function (res) {
                        if (res.success === 1) {
                            new GHAlert({
                                content: '账户添加成功！',
                                type: "success",
                                time: 2000
                            }).show();
                            render_subaccout();
                            $("#sub_name").val('');
                            $("#tel").val('');
                            $("#user_email").val('');
                            $("#password").val('');
                        }
                        else {
                            new GHAlert({
                                content: res.err_msg,
                                type: "fail",
                                time: 2000
                            }).show();
                        }
                    }
                 });
            }
        });
    });
});