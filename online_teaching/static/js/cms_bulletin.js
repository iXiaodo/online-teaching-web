$(function () {
    //显示添加公告modal
    $("#add_bulletin").click(function () {
        $("#add_bulletin-btn").modal('show');
    });
    var bulletin_author = $("#add_bulletin-btn h4").attr("data-author");
    var html_table = $("#bulletin-tbody");
    for(var i=0;i<html_table.children().length;i++){
        var pub_time = html_table.children().eq(i).children().eq(1).text();
        pub_time = pub_time.split('.')[0];
        html_table.children().eq(i).children().eq(1).html(pub_time);
    }


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
                        var pub_time = res["data"]["pub_time"];
                        insert_html += '<tr><td data-bulletin="'+bulletin_title+'" >'+bulletin_title+'</td>'
                        + '<td>'+pub_time+'</td>'
                        + '<td><span class="iconfont remove" style="cursor: pointer;" title="删除公告">&#xe609;</span>&nbsp;&nbsp;&nbsp;<span class="iconfont ban-ico" style="cursor: pointer;" title="禁用公告">&#xe6ab;</span></td></tr>';
                        $('#bulletin-tbody').children().eq(0).before(insert_html);
                        $("#add_bulletin-btn").modal('hide');
                        $('#add_bulletin-btn div input[name="bulletin-title"]').val('');
                        $('#textarea-input').val('');
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
            content: '确定删除公告'+bulletin_title+'吗？',
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
                                content: '删除角色成功',
                                type: "success",
                                time: 3000
                            }).show();
                            window.location = '/cms/bulletinPage/';
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
});