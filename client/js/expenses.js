(function($) {

	function loadMoreClickHandler() {
		$('#loadMore a').click(function() {
			$.mobile.showPageLoadingMsg();
			$.get($(this).attr('href'), 'offset=' + $(this).attr('data-offset'), function(data) {
				var ul = $('#expenseList');
				$('#loadMore').remove();
				ul.append(data);
				ul.listview('refresh');
				$.mobile.hidePageLoadingMsg();
				/* Element gets redrawn so call ourselves again. */
				loadMoreClickHandler();
			}).error(function() {
				alert('Something bad happend... Sorry.');
				$.mobile.hidePageLoadingMsg();
			});
			return false;
		});
	}

	$('#expenses').live('pageshow', function() {
		loadMoreClickHandler();
	});

})(jQuery);