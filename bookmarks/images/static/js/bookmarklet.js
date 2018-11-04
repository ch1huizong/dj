(function() {
		var jquery_version = '3.3.1';
		var site_url = 'http://127.0.0.1/';
		var static_urll = site_url + 'static/';
		var min_width = 100;
		var min_height = 100;
		
		function bookmarklet(msg){

		};

		//check if jQuery is loaded
		if (typeof window.jQuery != 'undefined'){
			bookmarklet();
		} else {
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
