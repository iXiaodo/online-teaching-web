
$(function(){
    //侧边栏样式
    $(".menu-item").removeClass("active");
    $("#consumer-manage").addClass("active be-click");
    $('#drop-business-content').css('display', 'block');
    $('#drop-business-content ul>li:eq(0)').css('background', '#4E5465');
    $('#drop-business-content ul>li:eq(0) a').css('color', 'white');

    $('#add_role').click(function(){
        $('#create_role_modal').modal('show');
    });

    $('#add_group').click(function(){
        $('#create_group_modal').modal('show');
    });

    var reg = /^[\u4e00-\u9fa5]|[0-9a-zA-Z]{1,8}$/;
    $('#save_btn').click(function(){
        var role_name = $('#create_role_modal div input[name="role-name"]').val();
        console.log(role_name);
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

    $('#save_group').click(function(){
        var group_name = $('#create_group_modal div input[name="group-name"]').val(),
            group_rank = $('#create_group_modal div input[name="rank-value"]').val(),
            role_name = $('#role tbody tr.success td:first').attr('data-name');

        if(!reg.test(group_name)){
            new GHAlert({
                content: "分组名称不符合规定",
                type: "fail",
                time: 2000
            }).show();
        }
        else if(!isPositiveInteger(group_rank) || parseInt(group_rank)<=1 || parseInt(group_rank)>=10){
            new GHAlert({
                content: "分组级别值不符合规定",
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
                    'group_name': group_name,
                    'rank': group_rank,
                    'action': 'add',
                    'type': 'group'
                }),
                success: function(res){
                    if(res.success===1){
                        new GHAlert({
                            content: "添加分组成功",
                            type: "success",
                            time: 2000
                        }).show();
                        $('#create_group_modal').modal('hide');
                        $('#create_group_modal div input[name="group-name"]').val('');
                        $('#create_group_modal div input[name="rank-value"]').val('');
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
   //get方法获取数据
    function get_role_and_group_info(role){
        $.ajax({
            url: '/cms/role_handler',
            type: 'get',
            cache: false,
            success: function(res){
                if(res.success===1){
                    var data = res.data,
                        insert_html = '',
                        right_html = '';
                    for(var key in data){
                        if(data[key]['type']==='preset'){
                            insert_html += '<tr><td data-name="'+key+'">'+key+'</td><td>默认</td><td></td></tr>';
                        }
                        else{
                            insert_html += '<tr><td data-name="'+key+'">'+key+'</td><td>自定义</td><td><span class="iconfont modify" title="修改角色名称" style="cursor: pointer;">&#xe738;</span>&nbsp;&nbsp;&nbsp;<span class="iconfont remove" title="删除角色" style="cursor: pointer;">&#xe609;</span></td></tr>';
                        }
                        if(role!==''){
                            key = role;
                        }
                        if(right_html===''){
                            if($.isEmptyObject(data[key]['own_groups'])){
                                right_html = '<tr><td colspan="4">管理角色负责整个系统的管理，没有分组的概念</td></tr>';
                            }
                            else{
                                for(var j in data[key]['own_groups']){
                                    if(data[key]['own_groups'][j]['type']==='preset'){
                                        right_html += '<tr><td data-name="'+j+'">'+j+'</td><td>'+data[key]['own_groups'][j]['rank']+'</td><td>默认</td><td></td></tr>';
                                    }
                                    else{
                                        right_html += '<tr><td data-name="'+j+'">'+j+'</td><td>'+data[key]['own_groups'][j]['rank']+'</td><td>自定义</td><td><span class="iconfont update" title="修改分组">&#xe738;</span>&nbsp;&nbsp;&nbsp;<span class="iconfont delete" title="删除分组">&#xe609;</span></td></tr>';
                                    }
                                }
                            }
                        }
                    }
                    if(role===''){
                        $('#role tbody').html(insert_html).find('tr:first').addClass('success');
                    }
                    else{
                        $('#role tbody').html(insert_html).find('tr td[data-name="'+role+'"]').parent().addClass('success');
                    }

                    $('#group tbody').html(right_html);

                    $('#role tbody').off('click', 'tr').on('click', 'tr', function(){
                        $(this).addClass('success').siblings('tr').removeClass('success');
                        var role = $(this).find('td:first').attr('data-name'),
                            write_html = '';
                        if($.isEmptyObject(res.data[role]['own_groups'])){
                            write_html = '<tr><td colspan="4">管理角色负责整个系统的管理，没有分组的概念</td></tr>';
                        }
                        else{
                            for(var i in res.data[role]['own_groups']){
                                if(res.data[role]['own_groups'][i]['type']==='preset'){
                                    write_html += '<tr><td data-name="'+i+'">'+i+'</td><td>'+res.data[role]['own_groups'][i]['rank']+'</td><td>默认</td><td></td></tr>';
                                }
                                else{
                                    write_html += '<tr><td data-name="'+i+'">'+i+'</td><td>'+res.data[role]['own_groups'][i]['rank']+'</td><td>自定义</td><td><span class="icon-font update" title="修改分组">&#xe684;</span><span class="icon-font delete" title="删除分组">&#xe60b;</span></td></tr>';
                                }
                            }
                        }
                        $('#group tbody').html(write_html);
                    });
                }
                else{
                    new GHAlert({
                        content: res.err_msg,
                        type: "fail",
                        time: 2000
                    }).show();
                    $('#role tbody').html('<tr><td colspan="3">获取数据失败</td></tr>');
                    $('#group tbody').html('<tr><td colspan="4">获取数据失败</td></tr>');
                }
            }
        })
    }
    get_role_and_group_info('');
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
                                get_role_and_group_info(new_value);
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


















