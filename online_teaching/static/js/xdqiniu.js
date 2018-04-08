/*
* @Author: xiaodong
* @Date:   2017-12-30 10:09:59
* @Last Modified by:   xiaodong
* @Last Modified time: 2017-12-30 10:43:38
*/
var xdqiniu = {
	'setUp':function(args) {
		var domain = "http://ozysh0j2y.bkt.clouddn.com/";
		var params = {
			runtimes: 'html5,flash,html4', //上传模式，依次退化
			max_file_size: '50mb', //文件最大允许的尺寸
			dragdrop: false, //是否开启拖拽上传
			chunk_size: '4mb', //分块上传时，每片的大小
			uptoken_url: '/common/get_token/', //ajax请求token的url
			domain: domain, //图片下载时候的域名
			get_new_uptoken: false, //是否每次上传文件都要从业务服务器获取token
			auto_start: true, //是否自动上传
			log_level: 5, //log级别
			init:{
				'FileUploaded': function(up,file,info) {
					if (args['success']) {
						var success = args['success'];
						file.name = domain + file.name;
						success(up,file,info);
					}
				},
				'Error': function(up,err,errTip) {
					if (args['error']) {
						var error = args['error'];
						error(up,err,errTip);
					}
				}
			},
		}
		for (var key in args) {
			params[key] = args[key];
		}
		var uploader = Qiniu.uploader(params);
		return uploader;
	}
}