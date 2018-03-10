$(function(){
    //侧边栏样式
    $(".menu-item").removeClass("active");
    $("#consumer-manage").addClass("active be-click");
    $('#drop-business-content').css('display', 'block');
    $('#drop-business-content ul>li:eq(1)').css('background', '#4E5465');
    $('#drop-business-content ul>li:eq(1) a').css('color', 'white');

    var subAccountData,
        bind_name='input';

    if(navigator.userAgent.indexOf("MSIE")!=-1) {
        bind_name='propertychange';
    }
    //即时搜索
    $("#search-sub-input").on(bind_name, function() {
        searchSubAccount();
    });
    $("#search-sub-btn").click(searchSubAccount);
    $("#sub-submit-btn").click(addAccountSubmit);

    $.ajax({
        url: "/cms/role_group_permission",
        type: "GET",
        success: function(res){
            var data = pagePermission(res.data.permission);
            var a_html = "";
            for (var i = 0; i < data.length; i++){
                a_html += '<div class="col-sm-6">' +
                    '<label>'+data[i][0]+' ： </label>' +
                    '<label><input type="radio" name="'+data[i][1]+'" value="w"> 写 </label>&nbsp;&nbsp;' +
                    '<label><input type="radio" name="'+data[i][1]+'" value="r"> 读 </label>&nbsp;&nbsp;' +
                    '<label><input type="radio" name="'+data[i][1]+'" value="no"> 无 </label>' +
                    '</div>';
            }
            $("#permission").html(a_html);

            var roles = res.data['roles'],
                insert_html = '',
                x = 1,
                current_role = '';
            for(var key in roles){
                if(current_role===''){
                    current_role = key;
                }
                insert_html += '<input type="radio" name="role" value="'+key+'" id="input'+x+'">&nbsp;<label for="input'+x+'">'+key+'</label>&nbsp;&nbsp;';
                x++;
            }
            $('#select_role').html(insert_html).find('input:first').prop('checked', true);

            if(!$.isEmptyObject(roles[current_role])){
                var insert_group = '';
                for(var i in roles[current_role]){
                    insert_group += '<input type="radio" value="'+roles[current_role][i]+'" id="group'+i+'" name="group">&nbsp;<label for="group'+i+'">'+roles[current_role][i]+'</label>&nbsp;&nbsp;';
                }
                $('#group').html(insert_group);
                $('#staff_position').removeClass('hidden');
            }

            //点击用户角色，业务流程权限变化
            $('#select_role').on('change','input[name="role"]',function () {
                var role = $(this).val();
                if(!$.isEmptyObject(roles[role])){
                    var insert_group = '';
                    for(var i in roles[role]){
                        insert_group += '<input type="radio" value="'+roles[role][i]+'" id="group'+i+'" name="group">&nbsp;<label for="group'+i+'">'+roles[role][i]+'</label>&nbsp;&nbsp;';
                    }
                    $('#group').html(insert_group);
                    $('#staff_position').removeClass('hidden');
                }
                else{
                    $('#group').empty();
                    $('#staff_position').addClass('hidden');
                }
            });
            subAccountInit('');
        }
    });

    function subAccountInit(name){
        $.ajax({
            url: "/cms/subaccount",
            type: "GET",
            cache: false,
            success: function(res){
                if(res.success == 1){
                    subAccountData = res.data;
                    renderSubAccountList(subAccountData,name);
                } else {
                    $("<li class='list-group-item'>获取数据失败:" + res.err_msg + "</li>").appendTo("#sub-account-list")
                }
            },
            error: function(){
                 $("<li class='list-group-item'>获取数据失败!</li>").appendTo("#sub-account-list");
            }
        })
    }

    $("#add-sub-btn").click(addSubAccount);

    /*渲染子账户列表*/
    function renderSubAccountList(subData,name){
        var count = 0;
        $("#sub-account-list").html(" ");
        $('#right-subaccount-info').removeClass('hidden');
        if(!$.isEmptyObject(subData)){
            $.each(subData,function(key,value){
                showAAccount(key,value);
                count++;
            });
            if(name){
                renderSubInfo(name)
            }
            else {
                renderSubInfo($(".list-group-item").first().find(".col-sm-offset-1").attr("subname"));
            }
        }
        else{
            $('#sub-submit-btn').removeClass('hidden');
            $('#password').val('');
            $('#user_email').val('');
            $('#right-subaccount-info').removeClass('hidden');
            $("#form1").find("input").attr("disabled",false);
            $('#select_role input[name="role"]:first').prop('checked', true);
            $("#sub-submit-btn").css("display","block");
            $("#password-con").css("display","block").val("");
            $("#editor-sub-btn").css("display","none");
            $(".list-group-item").removeClass("chosed-tenant");
        }
        adjustmentHeight("sub-account-list");

        /*绑定禁用子账户事件*/
        $(".disabled-account-btn").click(disabledAccount);

        $("#sub-account-list").children().click(function(){
            $(this).siblings().removeClass("chosed-tenant");
            var username = $(this).find(".col-sm-offset-1").attr("subname");
            renderSubInfo(username);
        })
    }

    /*渲染某个子账户的详细信息*/
    function renderSubInfo(subName){

        var jsonObj = subAccountData[subName];
        $('#close_add_page').hide();
        $('#select_role input, #permission input').removeProp('checked');
        $("#form1").find("input").attr("disabled",true);
        $("#editor-sub-btn").css("display","inline-block");
        $("#sub-submit-btn").css("display","none");
        $("#password-con").css("display","none").val(" ");

        /*突出是哪个子账户的详细信息*/
        $("div[subname="+subName+"]").parents(".list-group-item").addClass("chosed-tenant");

        $("#sub_name").val(subName);
        $("#user_name").val(jsonObj.user_name);
        $("#tel").val(jsonObj.tel);
        $("#user_email").val(jsonObj.user_email);


        $('#permission').find('input[value="no"]').prop('checked', true);

        for(var key in jsonObj.permission){
            if(jsonObj.permission[key]['w']){
                $('#permission').find('input[name="'+key+'"][value="w"]').prop('checked', true);
            }
            else if(!jsonObj.permission[key]['w']&&jsonObj.permission[key]['r']){
                $('#permission').find('input[name="'+key+'"][value="r"]').prop('checked', true);
            }
        }
        document.getElementById("status"+jsonObj.status).checked = true;

        $('#select_role input[value="'+jsonObj.role+'"]').trigger('change').prop('checked', true);
        $('#group input[value="'+jsonObj.group+'"]').prop('checked', true);
        $('#group input').attr('disabled', true);
    }

    $("#editor-sub-btn").click(function(){
        if($(this).hasClass('be_clicked')){
            $(this).removeClass('be_clicked');
            $("#form1").find("input, select").attr("disabled","disabled");
            $("#editor-sub-btn").css("display","inline-block");
            $("#sub-submit-btn").css("display","none");
            $("#password-con").css("display","none").val("");
        }
        else{
            $(this).addClass('be_clicked');
            $("#form1").find("input, select").attr("disabled",false);
            $("#sub_name, #user_name").attr("disabled","disabled");
            $("#sub-submit-btn").css("display","block").removeClass('hidden');
            $("#password-con").css("display","none").val("");
        }
    });

    /*动态展示一个子账户信息*/
    function showAAccount(subname,jsonObj) {
        var subStatus = jsonObj.status ? " ": " sub-account-disabled",
            target = $(".sub-account-disabled");

        var li = $('<li class="list-group-item'+ subStatus +'">'+
            '<div class="row">'+
            '<div class="col-sm-9 col-sm-offset-1" subname="'+ subname+'">'+ jsonObj.user_name +'</div>'+
            '<div class="col-sm-2 iconfont disabled-account-btn" title="禁用子账户" style="cursor: pointer;">&#xe6ab;</div>'+
        '</div>'+
        '</li>');
        if(target.length > 0){
            target.first().before(li);
        } else {
            $("#sub-account-list").append(li);
        }
    }

    /*搜索子账户*/
    function searchSubAccount() {
        var text = $("#search-sub-input").val(),
            reg = new RegExp(text),
            searchResult = {};

        $("#sub-account-list").html(" ");
        $.each(subAccountData,function(key,value){
            if(reg.exec(value.user_name)){
                searchResult[key] = value;
            }
        });
        renderSubAccountList(searchResult);
    }

    /*点击添加子账户时候的动作*/
    function addSubAccount(){
        $('#close_add_page').show();
        $('#sub-submit-btn').removeClass('hidden');
        $('#permission input').removeProp('checked');
        $('#select_role input[name="role"]:first').prop('checked', true);
        $("#form1").find("input").attr("disabled",false);
        $("#sub-submit-btn").css("display","block");
        $("#password-con").css("display","block").val("");
        $("#editor-sub-btn").css("display","none");
        $(".list-group-item").removeClass("chosed-tenant");
        document.getElementById("form1").reset();
    }

    //关闭添加子账户页面
    $('#close_add_page').click(function(){
       renderSubInfo($(".list-group-item").first().find(".col-sm-offset-1").attr("subname"));
    });

    /*提交添加子账户*/
    function addAccountSubmit(){
        var subData = {},
            data1 = {},
            permission_list = [];
        $('#permission input:checked').each(function(){
            var name = $(this).attr('name'),
                power = $(this).val();
            if(power!=='no'){
                permission_list.push([name, power]);
            }
        });
        subData.sub_name = $("#sub_name").val();
        subData.user_name = $("#user_name").val();
        subData.tel = $("#tel").val();
        subData.user_email = $("#user_email").val();
        subData.permission = permission_list;
        subData.role = $("input:radio[name='role']:checked").val();
        subData.group = $("#group input[name='group']:checked").val();
        subData.status = document.getElementById("statustrue").checked;
        subData.method = subAccountData[subData.sub_name]?"modify":"add";
        subData.password = subAccountData[subData.sub_name]?undefined:md5($("#password").val());

        /*检验输入格式*/
        if(!subData.sub_name.match(/^[0-9a-zA-Z]{1,16}$/)){
            new GHAlert({
                content: "登录名格式有误！登录名不能大于16位且只能包含数字和英文字母",
                type: "fail",
                time: 2000
            }).show();
            return false;
        }
        else if(!subData.user_name.match(/^[\u4e00-\u9fa5]|[0-9a-zA-Z]{3,16}$/)){
            new GHAlert({
                content: "昵称格式有误！昵称为3-16位且只能包含数字，英文，汉字",
                type: "fail",
                time: 2000
            }).show();
            return false;
        }
        else if(!subData.tel.match(/^1[0-9]{10}$/)){
            new GHAlert({
                content: "电话格式错误！请输入有效电话号码",
                type: "fail",
                time: 2000
            }).show();
            return false;
        }
        else if(!subData.user_email.match(/^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/)){
            new GHAlert({
                content: "邮箱格式错误！请输入有效邮箱",
                type: "fail",
                time: 2000
            }).show();
           return false;
        }
        else if(subData.permission.length===0){
            new GHAlert({
                content: "请至少选择一项个人权限",
                type: "fail",
                time: 2000
            }).show();
           return false;
        }

        var that = $(this);
        that.attr("disabled","disabled");
        $.ajax({
            type:"POST",
            url: "/cms/subaccount",
            data:{data: JSON.stringify(subData)},
            success: function (res){
                that.attr("disabled",false);
                if(res.success == 1){
                    $('#editor-sub-btn').removeClass('be_clicked');
                    new GHAlert({
                        content: res.data,
                        type: "success",
                        time: 2000
                    }).show();
                    subAccountInit(subData.sub_name);
                } else {
                    if (typeof(res.err_msg) != 'undefined'){
                        new GHAlert({
                            content: "操作失败！" + res.err_msg,
                            type: "fail",
                            time: 2000
                        }).show()
                    }
                    else{
                        new GHAlert({
                            content: "对不起，操作失败",
                            type: "fail",
                            time: 2000
                        }).show()
                    }
                }
            },
            error: function(){
                new GHAlert({
                    content: "对不起，请求异常！",
                    type: "fail",
                    time: 2000
                }).show()
            }
        })
    }


    /*从某分组删除某个子账号*/
    function disabledAccount() {
        if ($(this).parent().parent().hasClass('sub-account-disabled')){
            return;
        }
         var container = $(this).prev(),
             currentStatus = subAccountData[container.attr("subname")].status,
             sendData = {
                data: JSON.stringify({
                    sub_name: container.attr("subname"),
                    method: "ban",
                    status: !currentStatus
                })
             };
        zeroModal.confirm({
            content: '您确定要修改该子账号的禁用状态吗？',
            contentDetail: '提交后将会修改子账户之前的状态',
            transition: true,
            okFn: function() {
                update_status();
            },
            cancelFn: function() {}
        });
        function update_status(){
            $.ajax({
                type: "POST",
                url: '/cms/subaccount',
                data: sendData,
                success: function(res){
                    if(res.success == 1){
                        new GHAlert({
                            content: "禁用成功！",
                            type: "success",
                            time: 2000
                        }).show();
                        subAccountInit('');
                    } else {
                        new GHAlert({
                            content: "禁用失败！",
                            type: "fail",
                            time: 2000
                        }).show()
                    }
                }
            })
        }
    }

    function adjustmentHeight(targetId){
        /*IP，tenant列表部分滚动*/
        var max = document.getElementById("layout-aside").clientHeight -30-30-43-74;
        var currentHeight = document.getElementById(targetId).clientHeight;

        if(currentHeight > max){
            $("#"+targetId).css("height",max);
        }
    }
});