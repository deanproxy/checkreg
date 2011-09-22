function formatCurrency(num) {
	num = num.toString().replace(/\$|,/g, '');
	if (isNaN(num))
		num = "0";
	sign = (num == (num = Math.abs(num)));
	num = Math.floor(num * 100 + 0.50000000001);
	cents = num % 100;
	num = Math.floor(num / 100).toString();
	if (cents < 10)
		cents = "0" + cents;
	for (var i = 0; i < Math.floor((num.length - (1 + i)) / 3); i++)
		num = num.substring(0, num.length - (4 * i + 3)) + ',' + num.substring(num.length - (4 * i + 3));
	return (((sign) ? '' : '-') + '$' + num + '.' + cents);
}

function getTotal() {
	$.getJSON('/expenses/total/', function(data) {
		var totalArea = $('#total span');
		totalArea.html(formatCurrency(data.amount));
		if (data.amount < 0) {
			totalArea.removeClass('positive');
			totalArea.addClass('negative');
		} else {
			totalArea.removeClass('negative');
			totalArea.addClass('positive');
		}
	});
}

$(document).ready(function() {
	getTotal();
//	$('#goToExpenses').click(function(e) {
//		$.mobile.showPageLoadingMsg();
//		getExpenses(function() {
//			$.mobile.changePage('#expenses', {transition:'slide'});
//		});
//	});



	/* Refresh Total box */
	$('#total').click(function(e) {
		getTotal();
	});
});

/* Preload images */
var img1 = new Image('/static/images/spinner2.gif');
var img2 = new Image('/static/images/spinner.gif');
var img3 = new Image('/static/images/ajax-loader.gif');
var img4 = new Image('/static/images/loading.png');
var img5 = new Image('/static/images/check.png');
