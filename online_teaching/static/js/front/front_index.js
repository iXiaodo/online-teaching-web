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
                        insert_html += '<a href="/resource?page=1" class="look-download" target="_blank">查看与下载</a>';
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
    //渲染文章
    function  render_article_list() {
        var insert_html = '';
        $.ajax({
            url: '/get_articles',
            type:'GET',
            success: function(res){
                if(res.success===1){
                    var data = res['data'];
                    if(!$.isEmptyObject(data)){
                        for(var i in data){
                            insert_html += '<li class="list-group-item"><a href="/article_detail?article_id='+ data[i]['id']+'">'+ data[i]['title'] +'</a>&nbsp;&nbsp;<span class="update-time"><i class="iconfont">&#xe638;</i>更新时间：'+ data[i]['pub_time'] + '</span></li>';
                        }
                        insert_html += '<a href="/community?page=1" class="look-download" target="_blank">查看更多文章</a>';
                        $("#artilce-list").html(insert_html);
                    }else{
                        insert_html = '<li>还未发布文章，请等待发布！</li>';
                        $("#artilce-list").html(insert_html);
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
    render_article_list();
});