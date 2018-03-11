$(document).ready(function(){
    //前端页面展示权限
    function display_page_nav() {
        var permission_obj = ['roleGroupManage', 'accountPermissionManage', 'bulletinManage','topo','versionInfo'];
        for (var i in permission_obj){
            if (permission_obj[i] === 'roleGroupManage') {
                $('#role-group-manage').removeClass('hidden');
            }
            if (permission_obj[i] === 'accountPermissionManage') {
                $('#account-permission-manage').removeClass('hidden');
            }
            if (permission_obj[i] === 'bulletinManage') {
                $('#bulletin_manage').removeClass('hidden');
            }
            if (permission_obj[i] === 'topo') {
                $('#topo').removeClass('hidden');
            }
            if (permission_obj[i] === 'versionInfo') {
                $('#version-infomation').removeClass('hidden');
            }
        }
        //版本都可见
        $('#version').removeClass('hidden');

        var c_url = window.location.href;
        var c_index = -1;
        if (c_url.indexOf('/cms/role_group_manage')>0){
            c_index = 1;
        }
        if(c_url.indexOf('/cms/subAccount')>0){
            c_index = 2;
        }
        if(c_url.indexOf('/cms/bulletinPage/')>0){
            c_index = 3;
        }
        if(c_url.indexOf('/cms/version/')>0){
            c_index = 4;
        }
        console.log(c_index);
        if (c_index > 0){
            $('.side-menu').children().eq(c_index).addClass("active").siblings().removeClass("active");
        }
    }

display_page_nav();
getMathColor();
});

/*随机颜色*/
function getMathColor(){
    var arr = new Array();
    arr[0] = "#ffac13";
    arr[1] = "#83c44e";
    arr[2] = "#2196f3";
    arr[3] = "#e53935";
    arr[4] = "#00c0a5";
    arr[5] = "#16A085";
    arr[6] = "#ee3768";

    var le = $(".menu-item > a").length;
    for(var i=0;i<le;i++){
        var num = Math.round(Math.random()*5+1);
        var color = arr[num-1];
        $(".menu-item > a").eq(i).find("i:first").css("color",color);
    }
}

/*左侧菜单点击*/

/*获取宽度*/
function tabWidth(tabarr) {
    var allwidth = 0;
    $(tabarr).each(function() {
        allwidth += $(this).outerWidth(true)
    });
    return allwidth;
}

/*头部下拉框移入移出*/
$(document).on("mouseenter",".header-bar-nav",function(){
    $(this).addClass("open");
});
$(document).on("mouseleave",".header-bar-nav",function(){
    $(this).removeClass("open");
});

/*左侧菜单展开和关闭按钮事件*/
$(document).on("click",".layout-side-arrow",function(){
    if($(".layout-side").hasClass("close")){
        $(".layout-side").removeClass("close");
        $(".layout-main").removeClass("full-page");
        $(".layout-footer").removeClass("full-page");
    }else{
        $(".layout-side").addClass("close");
        $(".layout-main").addClass("full-page");
        $(".layout-footer").addClass("full-page");
    }
});

/*头部菜单按钮点击事件*/
$(".header-menu-btn").click(function(){
    $(".layout-side").removeClass("close");
    $(".layout-main").removeClass("full-page");
    $(".layout-footer").removeClass("full-page");
    $(".layout-side").slideToggle();
});

/*左侧菜单响应式*/
$(window).resize(function() {
    var width = $(this).width();
    if(width >= 750){
        $(".layout-side").show();
    }else{
        $(".layout-side").hide();
    }
});

/*获取cookie中的皮肤*/
function getSkinByCookie(){
    var v = getCookie("scclui-skin");
    var hrefStr=$("#layout-skin").attr("href");
    if(v == null || v == ""){
        v="qingxin";
    }
    if(hrefStr != undefined){
        var hrefRes=hrefStr.substring(0,hrefStr.lastIndexOf('skin/'))+'skin/'+v+'/skin.css';
        $("#skin").attr("href",hrefRes);
    }
}

$("#idc_ul").on("click","li",function(event){
    var name=$(event.currentTarget).find("a").attr("id");
    $.ajax({
        url:'/user/select_idc',
        type:'post',
        data:{idc:name},
        success:function(result){
            if(result.success==1){
                window.location.reload();
            }
            else{
                alert(result.err_msg);
            }
        },
        error:function(){
            $("#err_message").empty().text("对不起，读取数据错误").slideDown("500");
            setTimeout(function(){
                $("#err_message").slideUp('600');
            },2000)
        }
    })
})

//是否为正整数
function isPositiveInteger(s){
     var re = /^[0-9]+$/ ;
     return re.test(s)
}

function pagePermission(permission_list){
	var data = [];
	$.each(permission_list, function(key, value){
		if(value==='businessManage'){
			data.push(['业务管理', value]);
		}
		else if(value==='resourceManage'){
			data.push(['资源管理', value]);
		}
		else if(value==='subAccountManage'){
			data.push(['子账号管理', value]);
		}
		else if(value==='idcUserPage'){
			data.push(['用户页面管理', value]);
		}
		else{

        }
	});
	return data.reverse();
}

function ts_to_str(st){
	var date = new Date(st*1000);
	var Y = date.getFullYear() + '-';
	var M = (date.getMonth()+1 < 10 ? '0'+(date.getMonth()+1) : date.getMonth()+1) + '-';
	var D = (date.getDate() < 10 ? '0'+date.getDate() : date.getDate()) + ' ';
	var h = (date.getHours() < 10 ? '0'+date.getHours() : date.getHours()) + ':';
	var m = (date.getMinutes() < 10 ? '0'+date.getMinutes() : date.getMinutes()) + ':';
	var s = (date.getSeconds() < 10 ? '0'+date.getSeconds() : date.getSeconds());
	return (Y+M+D+h+m+s);
}