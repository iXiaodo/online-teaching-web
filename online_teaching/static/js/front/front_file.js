$(function () {
    //渲染需要分享的文件
    function  render_file_list() {
        var insert_html = '';
        $.ajax({
            url: '/resource_info',
            type:'GET',
            success: function(res){
                if(res.success===1){
                    var data = res['data'];
                    if(!$.isEmptyObject(data)){
                        for(var i in data){
                            insert_html += ' <li>&nbsp;&nbsp;<i class="iconfont">&#xe610;</i>&nbsp;<span class="title">' +data[i]['filename'] +
                                '</span><span class="up-time"><i class="iconfont">&#xe638;</i>上传时间：'+ data[i]['up_time'] +'</span><span class="author">'+
                                '<i class="iconfont">&#xe673;</i>上传作者：' + data[i]['author'] + '</span><a href="'+ data[i]['url'] +'" target="_blank">下载</a></li>';
                        }
                        $("#files-list-ul").html(insert_html);
                    }else{
                        insert_html = '<li>还未上传文件！请等待上传</li>';
                        $("#files-list-ul").html(insert_html);
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
    // render_file_list();
});