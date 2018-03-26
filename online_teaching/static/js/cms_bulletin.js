$(function () {
    //显示添加公告modal
    $("#add_bulletin").click(function () {
        $("#add_bulletin-btn").modal('show');
    });
    var bulletin_author = $("#add_bulletin-btn h4").attr("data-author");
    //初始化列表
    function get_bulletin_info() {
        $.ajax({
            url: '/cms/bulletinInfo/',
            cache: false,
            success: function(res){
                if(res.success===1){
                    var data = res.data;
                    if ($.isEmptyObject(data)){
                        var insert_html = '<tr><td></td><td>抱歉！还没有发布任何公告信息！</td><td></td></tr>>';
                        $('#bulletin-tbody').html(insert_html);
                    }else{
                        $("#right-subaccount-info").removeClass("hidden");
                        var insert_html = '';
                        for(var i in data){
                            var flag = data[i]['is_top'];
                            if(flag!==true){
                                insert_html += '<tr><td data-bulletin="'+i+'">'+i+'</td><td>'+data[i]['pub_time']+'</td>'
                                    +'<td><span class="iconfont remove" style="cursor: pointer;" title="删除公告">&#xe713;</span>&nbsp;&nbsp;&nbsp;'
                                    + '<span class="iconfont rename" style="cursor: pointer;" title="修改标题">&#xe63a;</span>&nbsp;&nbsp;&nbsp;'
                                    +'<span class="iconfont top" style="cursor: pointer;" title="置顶公告">&#xe637;</span></td></tr>';
                            }else{
                                insert_html += '<tr><td data-bulletin="'+i+'">'+i+'</td><td>'+data[i]['pub_time']+'</td>'
                                    +'<td><span class="iconfont remove" style="cursor: pointer;" title="删除公告">&#xe713;</span>&nbsp;&nbsp;&nbsp;'
                                    + '<span class="iconfont rename" style="cursor: pointer;" title="修改标题">&#xe63a;</span>&nbsp;&nbsp;&nbsp;'
                                    +'<span class="iconfont is-top" style="cursor: pointer;" title="取消置顶">&#xe636;</span></td></tr>';
                            }
                        }
                        $('#bulletin-tbody').html(insert_html);
                        $("#bulletin-tbody").children().eq(0).addClass("success");
                        var bulletin_title = $("#bulletin-tbody").children().eq(0).children().eq(0).attr("data-bulletin");
                        $("#bulletin-title").val(bulletin_title);
                        renderRadio(bulletin_title,data);
                    }
                }
                else{
                    new GHAlert({
                        content: res['err_msg'],
                        type: "fail",
                        time: 2000
                    }).show();
                }
            }
        });
    };
    get_bulletin_info();
    //添加公告
    var reg = /^[\u4e00-\u9fa5]|[0-9a-zA-Z]{1,12}$/;
    $("#save_btn").click(function () {
        var bulletin_title = $('#add_bulletin-btn div input[name="bulletin-title"]').val();
        var bulletin_content = $('#textarea-input').val();
        var insert_html = ''
        console.log(bulletin_author);
        if(!reg.test(bulletin_title)){
            new GHAlert({
                content: "公告标题不符合规定,请重新输入！",
                type: "fail",
                time: 2000
            }).show();
        }
        else{
            $.ajax({
                url: '/cms/bulletinInfo/',
                type:'post',
                dataType: 'json',
                contentType: 'application/json',
                data: JSON.stringify({
                    'bulletin_title': bulletin_title,
                    'bulletin_content': bulletin_content,
                    'action': 'add',
                    'type': 'bulletin',
                    'bulletin_author':bulletin_author
                }),
                success: function(res){
                    if(res.success===1){
                        new GHAlert({
                            content: "添加公告成功！",
                            type: "success",
                            time: 2000
                        }).show();
                        get_bulletin_info();
                        $('#add_bulletin-btn div input[name="bulletin-title"]').val('');
                        $('#textarea-input').val('');
                        $("#add_bulletin-btn").modal('hide');
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
    //删除公告
    $('#bulletin-tbody').on('click', 'span.iconfont.remove', function() {
        var first_td = $(this).parent().parent().find('td:first'),
            bulletin_title = first_td.attr('data-bulletin');
        zeroModal.confirm({
            content: '确定删除公告【'+bulletin_title+'】吗？',
            contentDetail: '提交后将会删除该公告的所有信息',
            transition: true,
            okFn: function() {
                $.ajax({
                    url: '/cms/bulletinInfo/',
                    type: 'post',
                    dataType: 'json',
                    contentType: 'application/json',
                    data: JSON.stringify({
                        'action': 'del',
                        'type': 'bulletin',
                        'bulletin_title': bulletin_title,
                        'bulletin_author':bulletin_author
                    }),
                    success: function (res) {
                        if (res.success === 1) {
                            new GHAlert({
                                content: '删除公告成功！',
                                type: "success",
                                time: 3000
                            }).show();
                            // window.location = '/cms/bulletinPage/';
                            get_bulletin_info();
                        }
                        else {
                            new GHAlert({
                                content: res.err_msg,
                                type: "fail",
                                time: 3000
                            }).show();
                        }
                    }
                })
            },
            cancelFn: function() {}
        });
    });
    //修改公告标题
    $('#bulletin-tbody').on('click', 'span.iconfont.rename', function() {
        var first_td = $(this).parent().parent().find('td:first'),
            bulletin_title = first_td.attr('data-bulletin');
        first_td.html('<input type="text" value="'+bulletin_title+'" style="width:80px;"><i class="iconfont cancel" title="取消">&#xe61d;</i>');
        first_td.find('input').off('keydown').on('keydown', function(e){
            if(e.keyCode===13){
                var new_value = $(this).val();
                if(new_value !== bulletin_title){
                    $.ajax({
                        url:'/cms/bulletinInfo/',
                        type:'post',
                        dataType:'json',
                        contentType:'application/json',
                        data: JSON.stringify({
                            'action': 'rename',
                            'type': 'bulletin',
                            'new_name': new_value,
                            'old_name': bulletin_title,
                            'bulletin_author':bulletin_author
                        }),
                        success: function(res){
                            if(res.success===1){
                                new GHAlert({
                                    content: '修改公告名称成功',
                                    type: "success",
                                    time: 2000
                                }).show();
                                first_td.html(new_value);
                                get_bulletin_info();
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
                    first_td.html(bulletin_title);
                }
            }
        });
        first_td.find('i').off('click').on('click', function(){
            first_td.html(bulletin_title);
        })
    });
    //置顶公告
    $('#bulletin-tbody').on('click', 'span.iconfont.top', function() {
        var first_td = $(this).parent().parent().find('td:first'),
            bulletin_title = first_td.attr('data-bulletin');
        zeroModal.confirm({
            content: '确定要置顶公告【'+bulletin_title+'】吗？',
            contentDetail: '提交后将会置顶此公告！',
            transition: true,
            okFn:function () {
                $.ajax({
                    url: '/cms/bulletinInfo/',
                    type: 'post',
                    dataType: 'json',
                    contentType: 'application/json',
                    data: JSON.stringify({
                        'action': 'top',
                        'type': 'bulletin',
                        'bulletin_title': bulletin_title,
                        'bulletin_author':bulletin_author
                    }),
                    success: function (res) {
                        if (res.success === 1) {
                            new GHAlert({
                                content: '公告置顶成功！',
                                type: "success",
                                time: 3000
                            }).show();
                            get_bulletin_info();
                        }
                        else {
                            new GHAlert({
                                content: res.err_msg,
                                type: "fail",
                                time: 3000
                            }).show();
                        }
                    }
                })
            },
            cancelFn:function () {

            }
        })
    });
    //取消置顶
    $('#bulletin-tbody').on('click', 'span.iconfont.is-top', function() {
        var first_td = $(this).parent().parent().find('td:first'),
            bulletin_title = first_td.attr('data-bulletin');
        zeroModal.confirm({
            content: '确定要取消公告【'+bulletin_title+'】的置顶状态吗？',
            contentDetail: '提交后此公告将不再置顶！',
            transition: true,
            okFn:function () {
                $.ajax({
                    url: '/cms/bulletinInfo/',
                    type: 'post',
                    dataType: 'json',
                    contentType: 'application/json',
                    data: JSON.stringify({
                        'action': 'cancel_top',
                        'type': 'bulletin',
                        'bulletin_title': bulletin_title,
                        'bulletin_author':bulletin_author
                    }),
                    success: function (res) {
                        if (res.success === 1) {
                            new GHAlert({
                                content: '取消置顶操作成功！',
                                type: "success",
                                time: 3000
                            }).show();
                            get_bulletin_info();
                        }
                        else {
                            new GHAlert({
                                content: res.err_msg,
                                type: "fail",
                                time: 3000
                            }).show();
                        }
                    }
                })
            },
            cancelFn:function () {

            }
        })
    });
    //渲染某个公告
    function  renderBulletin() {
        $('#bulletin-tbody').off('click','tr').on('click', 'tr', function() {
            $(this).addClass("success").siblings('tr').removeClass("success");
            var bulletin_title = $(this).find('td:first').attr("data-bulletin");
            $("#bulletin-title").val(bulletin_title);
            $.ajax({
                url: '/cms/bulletinInfo/',
                cache: false,
                success: function(res){
                    if(res.success===1){
                        var data = res.data;
                        if ($.isEmptyObject(data)){
                            new GHAlert({
                                content: '获取数据失败',
                                type: "fail",
                                time: 2000
                            }).show();
                        }else{
                            for(var i in data){
                                if(i===bulletin_title){
                                    renderRadio(i,data);
                                }
                            }
                        }
                    }
                    else{
                        new GHAlert({
                            content: res['err_msg'],
                            type: "fail",
                            time: 2000
                        }).show();
                    }
                }
            })
        });
    }
    renderBulletin();

    //修改公告
    $("#form1").find("input, select").attr("disabled","disabled");
    $("#sub-submit-btn").css("display","none");
    $("#bulletin-content").attr("readonly","readonly");
    $("#editor-sub-btn").click(function(){
        if($(this).hasClass('be_clicked')){
            $(this).removeClass('be_clicked');
            $("#form1").find("input").attr("disabled","disabled");
            $("#editor-sub-btn").css("display","inline-block");
            $("#sub-submit-btn").css("display","none");
            $("#bulletin-content").attr("readonly","readonly");
        }
        else{
            $(this).addClass('be_clicked');
            $("#status").find("input").removeAttr("disabled");
            $("#sub-submit-btn").css("display","block").removeClass('hidden');
            $("#bulletin-content").removeAttr("readonly");
        }
    });
    //提交修改内容
    $("#sub-submit-btn").click(function() {
        var content = $("#bulletin-content").val();
        var title = $("#bulletin-title").val();
        var is_active = $("input[name='status']:checked").val();
        if(content === '' || content === null){
            new GHAlert({
                content: "公告内容不能为空！",
                type: "fail",
                time: 2000
            }).show();
        }else {
            $.ajax({
                url: '/cms/bulletinInfo/',
                type: 'POST',
                dataType: 'json',
                contentType: 'application/json',
                data: JSON.stringify({
                    'action': 'modify',
                    'type': 'bulletin',
                    'bulletin_title': title,
                    'bulletin_author': bulletin_author,
                    'content':content,
                    'is_active':is_active
                }),
                success: function (res) {
                    if (res.success === 1) {
                        new GHAlert({
                            content: '公告内容更新成功！',
                            type: "success",
                            time: 3000
                        }).show();
                        get_bulletin_info();
                    }
                    else {
                        new GHAlert({
                            content: res.err_msg,
                            type: "fail",
                            time: 3000
                        }).show();
                    }
                }
            })
        }
    });
    // 渲染单选按钮的值
    function renderRadio(i,data) {
        $("#bulletin-content").val(data[i]['content']);
        var is_top = data[i]['is_top'];
        var is_active = data[i]['is_active'];
        if (is_top === true ){
            $("input[name=top-status][value=true]").prop("checked",true);
        }else{
            $("input[name=top-status][value=false]").prop("checked",true);
        }
        if(is_active ===true){
            $("input[name=status][value=true]").attr("checked",true);
        }else{
            $("input[name=status][value=false]").attr("checked",true);
        }
    }
});