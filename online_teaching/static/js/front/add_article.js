
$(function(){

});

$(function () {
    $(".header-h3 a").remove();


    //创建一个编辑器
    var E = window.wangEditor;
    var editor = new E('#editor');
    // 或者 var editor = new E( document.getElementById('editor') )
    editor.create();

    $("#btn-pub-article").on('click',function () {
        var title = $("#title").val();
        var category = $("#category-select").val();
        var desc = $("#desc").val();
        var content_html = editor.txt.html();
        if(title === '' || title === null){
            new GHAlert({
                content:'文章标题不能为空！',
                type:'fail',
                time:2000
            }).show();
        }else if(content_html.length <= 15){
            new GHAlert({
                content:'文章内容不能为空！',
                type:'fail',
                time:2000
            }).show();
        }else if(desc ==='' || desc === null){
            new GHAlert({
                content:'描述信息不能为空！',
                type:'fail',
                time:2000
            }).show();
        }else{
            $.ajax({
                url: '/add_article/',
                type: 'post',
                dataType: 'json',
                contentType: 'application/json',
                data: JSON.stringify({
                    'action': 'add_article',
                    'title':title,
                    'category':category,
                    'desc':desc,
                    'content_html':content_html
                }),
                success: function (res) {
                    if (res.success === 1) {
                        $("#title").val('');
                        $("#desc").val('');
                        $("#thumbnail").val('');
                        editor.txt.clear();
                        new GHAlert({
                            content: '恭喜您！文章添加成功！',
                            type: "success",
                            time: 2000
                        }).show();
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
        }
    });
});