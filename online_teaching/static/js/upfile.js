/*
* @Author: xiaodong
* @Date:   2017-12-25 15:19:55
* @Last Modified by:   xiaodong
* @Last Modified time: 2017-12-30 10:57:57
*/
$(function(){
    //七牛业务处理
    xdqiniu.setUp({
        'browse_button':'pickfiles',
        'success':function(up,file,info){
            //发送文件名到服务器
            var fileUrl = file.name;
            $("#pickfiles").attr('url-data',fileUrl);
            new GHAlert({
                content: '恭喜您！文件上传成功！',
                type: "success",
                time: 2000
            }).show();
        },
        'error':function(up,err,errTip){
            new GHAlert({
                content: errTip,
                type: "fail",
                time: 2000
            }).show();
        }
    });
    //渲染页面信息
    function render_file_list(url){
        var insert_html = '<li class="list-group-item">文件名称<span class="badge">操作</span></li>';
        $.ajax({
            url: '/cms/dataInfo/',
            cache: false,
            success: function(res){
                if(res.success===1){
                    var data = res.data;
                    if ($.isEmptyObject(data)){
                        insert_html = '<li class="list-group-item">很抱歉！您还没有上传资料</li>';
                        $("#file-list").html(insert_html);
                    }else{
                        for(var i in data){
                            insert_html += '<li class="list-group-item" file-name="'+ i+'" url-value="'+ data[i]['url'] +'">'+i+'<a href="'+data[i]['url']+'" class="badge iconfont download" style="cursor: pointer;" title="下载资料" target="_blank">&#xe684;</a>&nbsp;&nbsp;<span class="badge iconfont del" style="cursor: pointer;" title="删除资料">&#xe713;</span></li>'
                        }
                        $("#file-list").html(insert_html);
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
    }
    render_file_list();
    var reg = /^[\u4e00-\u9fa5]|[0-9a-zA-Z]{1,8}$/;
    $("#sub-account-block").off('click').on('click','span.iconfont.save-btn',function () {
        $("#add_file_modal").modal('show');

        $("#file_save_btn").off('click').on('click',function () {
            var file_url = $('#pickfiles').attr('url-data');
            var author = $("#sub-account-block").attr('author');
            var file_name = $("input[name='file-name']").val();
            if( !reg.test(file_name) ){
                new GHAlert({
                    content: '文件名称格式有误,请重新输入！',
                    type: "fail",
                    time: 2000
                }).show();
                $("input[name='file-name']").val('');
                return
            }else if(file_url===''||file_url===null||file_url===undefined){
                new GHAlert({
                    content: '文件获取出错',
                    type: "fail",
                    time: 2000
                }).show();
            }
            else if(author ==='' || author ===null || author===undefined){
                new GHAlert({
                    content: '获取作者出错！',
                    type: "fail",
                    time: 2000
                }).show();
                return
            }else if(file_name==='' || file_name ===null){
                new GHAlert({
                    content: '文件名称不能为空！',
                    type: "fail",
                    time: 2000
                }).show();
                return
            }else{
                $.ajax({
                    url: '/cms/dataInfo/',
                    type:'post',
                    dataType: 'json',
                    contentType: 'application/json',
                    data: JSON.stringify({
                        'action':'up_file',
                        'file_url':file_url,
                        'author':author,
                        'file_name':file_name
                    }),
                    success: function(res){
                        if(res.success===1){
                            new GHAlert({
                                content: "添加文件成功",
                                type: "success",
                                time: 2500
                            }).show();
                            $("#add_file_modal").modal('hide');
                            $('input[name="file-name"]').val('');
                            render_file_list();
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
            }
        });

    });

    //删除资料
    $("#file-list").on('click','span.badge.iconfont.del',function () {
        var th = $(this);
        var file_name = th.parent().attr('file-name');
        var author = $("#sub-account-block").attr('author');
        if(file_name===''||file_name===null){
            new GHAlert({
                content:'文件名称有误',
                type:'fail',
                time:2500
            }).show();
            return
        }
        zeroModal.confirm({
            content: '确定删除文件【'+file_name+'】吗？',
            contentDetail: '提交后将会删除该资料！',
            transition: true,
            okFn: function() {
                $.ajax({
                    url:'/cms/dataInfo/',
                    type:'post',
                    dataType: 'json',
                    contentType: 'application/json',
                    data : JSON.stringify({
                        'action':'del_file',
                        'file_name':file_name,
                        'author':author
                    }),
                    success:function (res) {
                        if(res.success===1){
                            new GHAlert({
                                content:'资料删除成功！',
                                type:'fail',
                                time:2500
                            }).show();
                            render_file_list();
                        }else{
                            new GHAlert({
                                content:res['err_msg'],
                                type:'fail',
                                time:2500
                            }).show();
                            return
                        }
                    },
                    error:function (res) {
                        new GHAlert({
                            content:res['err_msg'],
                            type:'fail',
                            time:2500
                        }).show();
                        return
                    }
                })
            },
            cancelFn: function() {}
        });
    });
});