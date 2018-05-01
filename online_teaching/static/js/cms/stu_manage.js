
$(function(){
    //侧边栏样式
    $(".menu-item").removeClass("active");
    $("#role-group-manage").addClass("active be-click");
    $('#add_role').click(function(){
        $('#create_role_modal').modal('show');
    });

    var reg = /^[\u4e00-\u9fa5]|[0-9a-zA-Z]{1,8}$/;
    //点击切换active
     $("#student tbody").off('click','tr').on('click','tr',function () {
        $(this).addClass('success').siblings('tr').removeClass('success');
     });
    //get方法获取数据
    function get_stu_info(){
        $.ajax({
            url: '/cms/stu_handler',
            type: 'get',
            cache: false,
            success: function(res){
                if(res.success===1){
                    var data = res.data,
                        insert_html = '';
                    if(!$.isEmptyObject(data)){
                        for(var key in data){
                            insert_html += '<tr><td data-email="'+data[key]['user_email']+'">'+data[key]['user_email']+'</td><td>'+data[key]['role']+'</td><td><span class="iconfont ban" title="禁用该学生" style="cursor: pointer;" data-id="'+data[key]['id']+'">&#xe6f2;</span></td></tr>';
                        }
                        $('#student tbody').html(insert_html).find('tr:first').addClass('success');
                    }else{
                        insert_html = '<tr><td></td><td>很抱歉！您没有查看此页面的权限</td><td></td></tr>';
                    }
                    $("#student tbody").html(insert_html);
                }
                else{
                    new GHAlert({
                        content: res.err_msg,
                        type: "fail",
                        time: 2000
                    }).show();
                    $('#student tbody').html('<tr><td colspan="3">获取数据失败</td></tr>');
                }
            }
        });
    }
    get_stu_info();

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


















