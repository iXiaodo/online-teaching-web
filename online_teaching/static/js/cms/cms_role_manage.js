
$(function(){
    //侧边栏样式
    $(".menu-item").removeClass("active");
    $("#role-group-manage").addClass("active be-click");
    $('#add_role').click(function(){
        $('#create_role_modal').modal('show');
    });

    $('#add_group').click(function(){
        $('#create_group_modal').modal('show');
    });
    var reg = /^[\u4e00-\u9fa5]|[0-9a-zA-Z]{1,8}$/;

    $('#save_btn').click(function(){
        var role_name = $('#create_role_modal div input[name="role-name"]').val();
        if(!reg.test(role_name)){
            new GHAlert({
                content: "角色名称不符合规定,请重新输入！",
                type: "fail",
                time: 2000
            }).show();
        }
        else{
            $.ajax({
                url: '/cms/role_handler',
                type:'post',
                dataType: 'json',
                contentType: 'application/json',
                data: JSON.stringify({
                    'role_name': role_name,
                    'action': 'add',
                    'type': 'role'
                }),
                success: function(res){
                    if(res.success===1){
                        new GHAlert({
                            content: "添加角色成功",
                            type: "success",
                            time: 2000
                        }).show();
                        $('#create_role_modal').modal('hide');
                        $('#create_role_modal div input[name="role-name"]').val('');
                        get_role_and_group_info(role_name);
                    }
                    else{
                        new GHAlert({
                            content: res.err_msg,
                            type: "fail",
                            time: 2000
                        }).show();
                    }
                }
            })
        }
    });
    //点击切换active
     $("#role tbody").off('click','tr').on('click','tr',function () {
        $(this).addClass('success').siblings('tr').removeClass('success');
     });
    //get方法获取数据
    function get_role_info(){
        $.ajax({
            url: '/cms/role_handler',
            type: 'get',
            cache: false,
            success: function(res){
                if(res.success===1){
                    var data = res.data,
                        insert_html = '';
                    if(data['permission'] === 'super_admin'){
                        for(var key in data['roles']){
                            insert_html += '<tr><td data-name="'+data['roles'][key]+'">'+data['roles'][key]+'</td><td>默认</td><td><span class="iconfont modify" title="修改角色名称" style="cursor: pointer;">&#xe63a;</span>&nbsp;&nbsp;&nbsp;<span class="iconfont remove" title="删除角色" style="cursor: pointer;">&#xe713;</span></td></tr>';
                        }
                    }else{
                        insert_html = '<tr><td></td><td>很抱歉！您没有查看此页面的权限</td><td></td></tr>';
                    }
                    $('#role tbody').html(insert_html).find('tr:first').addClass('success');
                }
                else{
                    new GHAlert({
                        content: res.err_msg,
                        type: "fail",
                        time: 2000
                    }).show();
                    $('#role tbody').html('<tr><td colspan="3">获取数据失败</td></tr>');
                }
            }
        })
    }
    get_role_info();

    //角色名称修改
    $('#role tbody').on('click', 'span.iconfont.modify', function(){
        var first_td = $(this).parent().parent().find('td:first'),
            role_name = first_td.attr('data-name');
        first_td.html('<input type="text" value="'+role_name+'" style="width:80px;"><i class="icon-font cancel" title="取消">&#xe61d;</i>');
        first_td.find('input').off('keydown').on('keydown', function(e){
            if(e.keyCode===13){
                var new_value = $(this).val();
                if(new_value !== role_name){
                    $.ajax({
                        url:'/cms/role_handler',
                        type:'post',
                        dataType:'json',
                        contentType:'application/json',
                        data: JSON.stringify({
                            'action': 'modify',
                            'type': 'role',
                            'new_name': new_value,
                            'old_name': role_name
                        }),
                        success: function(res){
                            if(res.success===1){
                                new GHAlert({
                                    content: '修改角色名称成功',
                                    type: "success",
                                    time: 2000
                                }).show();
                                first_td.html(new_value);
                                get_role_info();
                            }
                            else{
                                new GHAlert({
                                    content: res.err_msg,
                                    type: "fail",
                                    time: 2000
                                }).show();
                            }
                        }
                    })
                }
                else{
                    first_td.html(role_name);
                }
            }
        });
        first_td.find('i').off('click').on('click', function(){
            first_td.html(role_name);
        })
    });

    //角色删除
    $('#role tbody').on('click', 'span.iconfont.remove', function() {
        var first_td = $(this).parent().parent().find('td:first'),
            role_name = first_td.attr('data-name');

        zeroModal.confirm({
            content: '确定删除角色'+role_name+'吗？',
            contentDetail: '提交后将会删除该角色的所有信息',
            transition: true,
            okFn: function() {
                $.ajax({
                    url: '/cms/role_handler',
                    type: 'post',
                    dataType: 'json',
                    contentType: 'application/json',
                    data: JSON.stringify({
                        'action': 'del',
                        'type': 'role',
                        'role_name': role_name
                    }),
                    success: function (res) {
                        if (res.success === 1) {
                            new GHAlert({
                                content: '删除角色成功',
                                type: "success",
                                time: 2000
                            }).show();
                            get_role_and_group_info('');
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

    //分组修改
    $('#group tbody').on('click', 'span.iconfont.update', function(){
        var first_td = $(this).parent().parent().find('td:first'),
            next_td = $(this).parent().parent().find('td:eq(1)'),
            group_name = first_td.attr('data-name'),
            rank = next_td.text(),
            role_name = $('#role tbody tr.success td:first').attr('data-name');

        $('#update_group_modal').modal('show');
        $('#update_group_modal div input[name="group-name"]').val(group_name);
        $('#update_group_modal div input[name="rank-value"]').val(rank);

        $('#update_group').unbind('click').click(function(){
            var new_group = $('#update_group_modal div input[name="group-name"]').val(),
                new_rank = $('#update_group_modal div input[name="rank-value"]').val();

            if(new_group !== group_name || new_rank !== rank){
                $.ajax({
                    url:'/cms/role_handler',
                    type:'post',
                    dataType:'json',
                    contentType:'application/json',
                    data: JSON.stringify({
                        'action': 'modify',
                        'type': 'group',
                        'new_group': new_group,
                        'new_rank': new_rank,
                        'old_group': group_name,
                        'role_name': role_name
                    }),
                    success: function(res){
                        if(res.success===1){
                            new GHAlert({
                                content: '修改分组名称成功',
                                type: "success",
                                time: 2000
                            }).show();
                            $('#update_group_modal').modal('hide');
                            get_role_and_group_info(role_name);
                        }
                        else{
                            new GHAlert({
                                content: res.err_msg,
                                type: "fail",
                                time: 2000
                            }).show();
                        }
                    }
                })
            }
            else{
                $('#update_group_modal').modal('hide');
            }
        });

    });

    //分组删除
    $('#group tbody').on('click', 'span.iconfont.delete', function() {
        var first_td = $(this).parent().parent().find('td:first'),
            group_name = first_td.attr('data-name'),
            role_name = $('#role tbody tr.success td:first').attr('data-name');

        zeroModal.confirm({
            content: '确定删除分组'+group_name+'吗？',
            contentDetail: '提交后将会删除该分组信息',
            transition: true,
            okFn: function() {
                $.ajax({
                    url: '/cms/role_handler',
                    type: 'post',
                    dataType: 'json',
                    contentType: 'application/json',
                    data: JSON.stringify({
                        'action': 'del',
                        'type': 'group',
                        'role_name': role_name,
                        'group_name': group_name
                    }),
                    success: function (res) {
                        if (res.success === 1) {
                            new GHAlert({
                                content: '删除分组成功',
                                type: "success",
                                time: 2000
                            }).show();
                            get_role_and_group_info(role_name);
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

});


















