$(document).ready(function(){

/* 
 * add likes
*/
$('#likes').click(function(){
	var catid;
	catid = $(this).attr('data-catid');
	$.get('/rango/like_category/', { category_id: catid}, function(data){
		$('#like_count').html(data);
		$('#likes').hide();
	});
});

/*
 *  add suggestion
 */
$('#suggestion').keyup(function(){
	var query;
	query = $(this).val();
	$.get('/rango/suggest_category/', {suggestion: query}, function(data){
		$('#cats').html(data);
	});
});

/*
 *  Add pages
 */
$('.rango-add').click(function(){
	var catid = $(this).attr('data-catid');
	var url = $(this).attr('data-url');
	var title = $(this).attr('data-title');
	var me = $(this);
	
	$.get('/rango/auto_add_page/',{ category_id: catid, url: url, title: title },function(data){
		$('#pages').html(data);
		me.hidden();
	});
});

});
