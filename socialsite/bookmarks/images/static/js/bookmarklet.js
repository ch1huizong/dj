(function(){
	var jquery_version = '3.2.1';
	var site_url = 'http://127.0.0.1:8000/';
	var static_url = site_url + 'static/';
	var min_width = 100;
	var min_height = 100;

	function bookmarklet(msg){  //功能函数
		//加载css
		var css = jQuery('<link>');
		css.attr({
			rel: 'stylesheet',
			type: 'text/css',
			href: static_url + 'css/bookmarklet.css?r=' + Math.floor(Math.random()*99999999999999999)
		});
		jQuery('head').append(css);

		//加载html
		box_html = '<div id="bookmarklet"><a href="#" id="close">&times;</a><h1>Select an image to bookmark:</h1><div class="images"></div></div>';
		jQuery('body').append(box_html);

		//close事件
		jQuery('#bookmarklet #close').click(function(){
			jQuery('#bookmarklet').remove(); //删除bookmarklet元素
		});

		//寻找所有的图片并且展示它们
		jQuery.each(jQuery('img[src$="jpg"]'), function(index, image){
			if (jQuery(image).width() >= min_width && jQuery(image).height() >= min_height){
				image_url = jQuery(image).attr('src');
				jQuery('#bookmarklet .images').append('<a href="#"><img src="' + image_url + '" /></a>');
			}
		});

		//当一个图片被选择的时候，打开它的url在新窗口
		jQuery('#bookmarklet .images a').click(function(e){
			selected_image = jQuery(this).children('img').attr('src');
			jQuery('#bookmarklet').hide();  //隐藏内容块
			//新窗口打开
			window.open(site_url + 'images/create/?url='
						+ encodeURIComponent(selected_image)
						+ '&title='
						+ encodeURIComponent(jQuery('title').text()),
						'_blank');
		});


	};

	if (typeof window.jQuery != 'undefined'){ //直接调用
		bookmarklet(); 
	}else {   //加载jQuery并调用bookmarklet
		var conflict = typeof window.$ != 'undefined';
		var script = document.createElement('script');
		script.setAttribute('src',
		'https://cdn.bootcss.com/jquery/3.2.1/jquery.min.js');
		document.getElementsByTagName('head')[0].appendChild(script);

		var attempts = 15;
		(function(){
			if (typeof window.jQuery == 'undefined'){
				if(--attempts > 0){
					window.setTimeout(arguments.callee, 250);
				}else{
					alert('An error occurred while loading jQuery.');
				}
			}else{
				bookmarklet();
			}
		})();
	}
})();
