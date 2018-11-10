(function(){
	if (window.myBookmarklet !== undefined){
		myBookmarklet();
	} else {
		document.body.appendChild(document.createElement('script')).src='https://e5bd050d.ngrok.io/static/js/bookmarklet.js?
		r='+ Math.floor(Math.random()*999999999999999999999);
	}
}

)();
