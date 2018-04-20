$(document).ready(function() {
    //左侧目录按钮样式
    $(".subnav-box ul li").click(function () {
        $(this).css("background-color"," #f0f0f0").siblings().css("background-color","");
    });
    //切换界面样式
    var c_url = window.location.href;
    if(c_url.indexOf("/course_intro") > 0){
        $(".subnav-box ul").children().eq(0).css("background-color"," #f0f0f0").siblings().css("background-color","");
    }else if(c_url.indexOf("/course_develop") > 0){
        $(".subnav-box ul").children().eq(1).css("background-color"," #f0f0f0").siblings().css("background-color","");
    }else if(c_url.indexOf("/course_teachers") > 0){
        $(".subnav-box ul").children().eq(2).css("background-color"," #f0f0f0").siblings().css("background-color","");
    }
});