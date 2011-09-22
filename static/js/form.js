(function($) {

	$(document).ready(function() {
		$('form').validate({
			submitHandler: function(form) {
				$.mobile.showPageLoadingMsg();
				$.post($(form).attr('action'), $(form).serialize(), function(data, textStatus) {
					getTotal();
					if (form.name === 'update') {
						$.mobile.changePage('/expenses/list/', {transition:'slideright'});
					} else {
						$.mobile.changePage('/expenses/index/', {transition:'slidedown'});
					}
				}).error(function() {
					alert('Oops. Could not create.');
					$.mobile.hidePageLoadingMsg();
				});
				return false;
			}
		});

		$('#saveExpense').click(function() {
			$('#updateExpense').submit();
		});
		$('#deleteExpense').click(function() {
			if (confirm('Want to kill this expense?')) {
				var id = $('input[name=id]').val();
				$.post('/expenses/delete/' + id, {}, function() {
					$.mobile.changePage('/expenses/list/', {transition:'slideright'});
				}).error(function() {
					alert('Some sort of error occured. Did not delete.');
				});
			}
		});
	});
})(jQuery);