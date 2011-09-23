(function($) {

	function loadMoreClickHandler() {
		$('#loadMore').click(function() {
			$.mobile.showPageLoadingMsg();
			$.get('/expenses/more/', function(data) {
				var ul = $(this).parent('ul');
				$(this).remove();
				ul.append(data);
				ul.listview('refresh');
				$.mobile.hidePageLoadingMsg();
				loadMoreClickHandler();
			});
		});
	}

	$('#list').live('pageshow', function() {
		loadMoreClickHandler();
	});

})(jQuery);