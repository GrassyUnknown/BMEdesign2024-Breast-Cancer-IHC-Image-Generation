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
	let allFiles = ['\\00000_test_1+.png','\\00001_test_2+.png','\\00002_test_2+.png','\\00003_test_3+.png','\\00004_test_0.png','\\00005_test_1+.png','\\00006_test_3+.png','\\00007_test_1+.png','\\00008_test_3+.png','\\00009_test_2+.png','\\00010_test_1+.png','\\00011_test_3+.png','\\00012_test_1+.png','\\00013_test_0.png','\\00014_test_2+.png','\\00015_test_1+.png','\\00016_test_1+.png','\\00017_test_1+.png','\\00018_test_2+.png','\\00019_test_2+.png','\\00020_test_1+.png']
	let timeout = 3000 + Math.random() * 12000;
	for(let i = 0; i < allFiles.length; i++){
		if(allFiles[i] === fileName){
			let src2 = './static/images/result' + fileName;
			setTimeout(()=>{
				$('#img-avatar-2').attr('src', src2); //将图片地址放置在img的src中。
			},timeout)
			
			return ;
		}
	}
	setTimeout(()=>{
		$('#img-avatar-2').attr('src', './static/images/result/error.png');
	},timeout)
	return ;	
});
})


