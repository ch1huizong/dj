(function() {
		var jquery_version = '3.3.1';
		var site_url = 'http://127.0.0.1/';
		var static_url = site_url + 'static/';
		var min_width = 100;
		var min_height = 100;
		
		function bookmarklet(msg){
			//load css
			var css = jQuery('<link>');
			css.attr({
				rel: 'stylesheet',
				type: 'text/css',
				href: static_url + 'css/bookmarklet.css?r=' + Math.floor(Math.random() * 99999999999999999)
			});
			jQuery('head').append(css);

			//load html
			box_html = '<div id="bookmarklet"><a href="#" id="close">&times;</a><h1>Select an image to bookmark:</h1><div class="images"></div></div>'
			jQuery('body').append(box_html);
			
			//close event
			jQuery('#bookmarklet #close').click(function(){
				jQuery('#bookmarklet').remove();
			});

			//find images and display them
			jQuery.each(jQuery('img[src$="jpg"]'), function(index, image){
				if (jQuery(image).width() >= min_width && jQuery(image).height() >= min_height){
					image_url = jQuery(image).attr('src');
					jQuery('#bookmarklet .images').append('<a href="#"><img src="' + 
					image_url + '" /></a>');
				}
			});

			// when an image is selected
			jQuery('#bookmarklet .images a').click(function(e){
				selected_image = jQuery(this).children('img').attr('src');
				//hide bookmarklet
				jQuery('#bookmarklet').hide();
				window.open(site_url + 'images/create/?url='
										+ encodeURIComponent(selected_image)
										+ '&title='
										+ encodeURIComponent(jQuery('title').text()),
										'_blank');
			});

		};

		//check if jQuery is loaded
		if (typeof window.jQuery != 'undefined'){
			bookmarklet();
		} else {
			// check conflict
			var conflict = typeof window.$ != 'undefined';

			//create the script and point to bootcdn
			var script = document.createElement('script');
			script.src = 'https://cdn.bootcss.com/jquery/' + jquery_version + '/jquery.min.js';
			document.head.appendChild(script)

			//create a way to wait until script loading
			var attempts = 15;
			(function(){
				if (typeof window.jQuery == 'undefined'){
					if (--attempts > 0){
						//call himeself in a few milliseconds
						window.setTimeout(arguments.callee, 250);
					} else {
						alert('An error occurred while loading jQuery')
					}
				} else {
					bookmarklet();
				}
			})();
	}
})();
