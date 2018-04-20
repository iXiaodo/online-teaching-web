$(function () {
    //渲染需要分享的文件
    function  render_file_list() {
        var insert_html = '';
        $.ajax({
            url: '/get_file',
            type:'GET',
            success: function(res){
                if(res.success===1){
                    var data = res['data'];
                    if(!$.isEmptyObject(data)){
                        for(var i in data){
                            insert_html += '<li class="list-group-item">'+ data[i]['filename'] +'&nbsp;&nbsp;<span class="update-time"><i class="iconfont">&#xe638;</i>更新时间：'+ data[i]['up_time'] + '</span></li>';
                        }
                        insert_html += '<a href="/resource" class="look-download" target="_blank">查看与下载</a>';
                        $("#file-download-list").html(insert_html);
                    }else{
                        insert_html = '<li>还未上传文件！请等待上传</li>';
                        $("#file-download-list").html(insert_html);
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

});