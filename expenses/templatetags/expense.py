from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.filter
def format_amount(amount, show_negative=True):
	"""
	amount is a float type and may be negative. When displaying, we don't want
	a negative value displayed and we also only want 2 decimal points.
	"""

	if not show_negative and amount < 0:
		amount -= amount * 2
	return "%.2f" % amount

@register.filter
def set_checked_if_deposit(amount):
	""" returns the 'checked' attribute if amount is >= 0 """

	checked = ''
	if amount >= 0:
		checked = 'checked'
	return checked

@register.filter
def amount_type(amount):
	""" positive or negative? """

	type = 'negative'
	if amount >= 0:
		type = 'positive'

	return type


@register.simple_tag(takes_context=True)
def date_divider(context, date):
	""" display the date divider if it differs from the last date """

	datestr = date.strftime("%b %d, %Y")
	html = ''
	if 'last_date' not in context.dicts[0] or context.dicts[0]['last_date'] != datestr:
		html = '<li data-role="list-divider">%s</li>' % datestr
		context.dicts[0]['last_date'] = datestr

	return html