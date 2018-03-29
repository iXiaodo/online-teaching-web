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
			console.log('file uploaded-----------');
				//发送文件名到服务器
			// $('#pickfiles').attr('src',file.name);
            console.log(file.name);
		},
		'error':function(){
			console.log('error:'+err);
		}
	})
	//按钮点击事件
	$('.submit-btn').click(function(event){
		event.preventDefault();

		$.post({
        });
	});
});