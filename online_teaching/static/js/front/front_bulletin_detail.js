$(function () {
    var title = getUrlRequest()['title'];
    $.ajax({
        url: '/bulletin?title=' + title,
        success:function(res){
            if(res.success === 1){
                var data = res.data;
                if(!$.isEmptyObject(data)){

                }
                else{
                    new GHAlert({
                        content: '',
                        type: "fail",
                        time: 2000
                    }).show()
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
});