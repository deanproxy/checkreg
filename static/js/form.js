(function($) {

	$('.form').live('pageshow', function(event) {
		$('form').validate({
			submitHandler: function(form) {
				$.mobile.showPageLoadingMsg();
				$.post($(form).attr('action'), $(form).serialize(), function(data, textStatus) {
					getTotal();
					history.back();
				}).error(function() {
					alert('Oops. Could not create.');
					$.mobile.hidePageLoadingMsg();
				});
				return false;
			}
		});

		$('#saveUpdateExpense').click(function() {
			$('#updateExpense').submit();
		});
		$('#deleteExpense').click(function() {
			if (confirm('Want to kill this expense?')) {
				var id = $('input[name=id]').val();
				var csrf_token = $('input[name=csrfmiddlewaretoken]').val();
				$.post('/expenses/delete/' + id, {'csrfmiddlewaretoken':csrf_token}, function() {
					getTotal();
					history.back();
				}).error(function() {
					alert('Some sort of error occured. Did not delete.');
					$.mobile.hidePageLoadingMsg();
				});
			}
			return false;
		});
	});

})(jQuery);