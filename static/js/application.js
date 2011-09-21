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

var lastExpenseDate = null;
function displayExpenses(data, start, total) {
	var ul = $('#expenses ul');
	if (start == 0) {
		ul.html('');
	} else {
		ul.find('#loadMore').remove();
	}
	for (i = 0; i < data.expenses.length; i++) {
		var expense = data.expenses[i];
		var formattedAmount = expense.amount
		if (!lastExpenseDate || lastExpenseDate != expense.createdAt) {
			ul.append('<li data-role="list-divider">' + expense.createdAt + '</li>');
			lastExpenseDate = expense.createdAt;
		}
		line = '<li>' + expense.description + '<span class="ui-li-count ';
		if (expense.amount > 0) {
			line += 'positive';
		} else {
			line += 'negative'
		}
		line += '">';
		line += formatCurrency(expense.amount);
		line += '</span>'
		line += '<div id="' + expense.id + '" class="deleteButton">Delete</div>';
		line += '</li>';
		ul.append(line);
	}
	$('#expenses ul li').bind('swiperight', function(e) {
		$('.deleteButton').hide();
		var button = $(this).child('a');
		button.show();
	});
	$('a.deleteButton').click(function() {
		var a = $(this);
		a.parent('li').hide();
		$.ajax({
			url: '/expenses/delete/' + a.attr('id'),
			error: function() {
				a.parent('li').show();
				alert('Oops! Can not delete');
			},
			success: function() {
				getTotal();
			}
		});
	});
	if (start + total < data.total) {
		remainingTotal = data.total - (start + total);
		ul.append('<li id="loadMore"><a href="#">Load More Expenses... <div>' + remainingTotal +
				' expenses remaining, ' + data.total + ' total</div></a></li>');
		ul.find('#loadMore a').click(function() {
			$.mobile.showPageLoadingMsg();
			start += total;
			$.getJSON('/expenses/list/', {offset:start,max:total}, function(data) {
				displayExpenses(data, start, total);
				$.mobile.hidePageLoadingMsg();
			});
		});
	}
}

function getExpenses(callback) {
	$.getJSON('/expenses/list/', {offset:0, max:30}, function(data) {
		displayExpenses(data, 0, 30);
		callback();
	});
}

function getTotal(callback) {
	if (!callback) {
		/* If callback wasn't provided, make it empty */
		callback = function() {};
	}
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
		callback();
	});
}

$.fn.highlight = function(toColor) {
	var elem = $(this);
	var oldColor = { backgroundColor: elem.css('background-color') };
	return elem.show().css('background-color', toColor).
			animate(oldColor, {duration:800});
}

$(document).ready(function() {
	getTotal();
	$('#goToExpenses').click(function(e) {
		$.mobile.showPageLoadingMsg();
		getExpenses(function() {
			$.mobile.changePage('#expenses', {transition:'slide'});
		});
	});

	$('#form').validate({
		submitHandler: function(form) {
			$.mobile.showPageLoadingMsg();
			$.post($('#form').attr('action'), $(form).serialize(), function(data, textStatus) {
				getTotal();
				$('.progress').hide();
				$.mobile.changePage('#home', {transition:'slidedown'});
				/* Reset form */
				$('input[name=description]').val('');
				$('input[name=amount]').val('');
				$('input[name=deposit]').val('');
			}).error(function() {
				alert('Oops. Could not create.');
				$.mobile.hidePageLoadingMsg();
			});
			return false;
		}
	});

	/* Make the checkbox work */
	$('ul li.checkrow div').click(function(e) {
		$(this).highlight('#194fdb');
		$(this).toggleClass('active');
		if ($(this).hasClass('active')) {
			$('input[name=deposit]').val('true');
		} else {
			$('input[name=deposit]').val('');
		}
	});

	/* Refresh Total box */
	$('#total').click(function(e) {
		var that = this;
		getTotal(function() {
			$(that).highlight('#194fdb');
		});
	});
});

/* Preload images */
var img1 = new Image('/static/images/spinner2.gif');
var img2 = new Image('/static/images/spinner.gif');
var img3 = new Image('/static/images/ajax-loader.gif');
var img4 = new Image('/static/images/loading.png');
var img5 = new Image('/static/images/check.png');
