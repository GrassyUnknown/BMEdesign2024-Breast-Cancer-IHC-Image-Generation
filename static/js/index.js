window.HELP_IMPROVE_VIDEOJS = false;


$(document).ready(function() {
    // Check for click events on the navbar burger icon
    var options = {
			slidesToScroll: 1,
			slidesToShow: 1,
			loop: true,
			infinite: true,
			autoplay: true,
			autoplaySpeed: 5000,
    }

		// Initialize all div with carousel class
    var carousels = bulmaCarousel.attach('.carousel', options);
	
    bulmaSlider.attach();

$("#chooseImage").on('change',function(){
	let filePath = $(this).val(); //获取到input的value，里面是文件的路径
	
	let fileFormat = filePath.substring(filePath.lastIndexOf(".")).toLowerCase(); //获取文件后缀
	let src = window.URL.createObjectURL(this.files[0]); //转成可以在本地预览的格式

	// 检查是否是图片
	if( !fileFormat.match(/.png|.jpg|.jpeg|.bmp/) ) {
		//error_prompt_alert
		alert('上传错误,文件格式必须为：png/jpg/jpeg/bmp');
		return ;
	}
	$('#img-avatar').attr('src', src); //将图片地址放置在img的src中。
	let fileName = filePath.substring(filePath.lastIndexOf('\\'));
	$('#img-avatar-2').attr('src', './static/images/loading.gif'); //将图片地址放置在img的src中。
	var pic1 = this.files[0];
    var formData = new FormData();
    formData.append('file',pic1);
	let xhr = new XMLHttpRequest();
	xhr.open('post','http://60.205.127.51:6789/getpic' , true);
	xhr.responseType = 'blob' ;
	xhr.send(formData);// 发送ajax请求
	xhr.onreadystatechange = function () {
		if (xhr.readyState === XMLHttpRequest.DONE) {
			console.log(xhr.response);
			let src = window.URL.createObjectURL(new File([xhr.response],"output.png",{type: "image/png"})); //转成可以在本地预览的格式
			$('#img-avatar-2').attr('src', src); //将图片地址放置在img的src中。
		}
	};
	return ;	
});
})


