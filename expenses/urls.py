from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
	url(r'^list/', 'expenses.views.list', name='list_expenses_url'),
	url(r'^more/', 'expenses.views.more', name='more_expenses_url'),
	url(r'^total/', 'expenses.views.total', name='total_url'),
	url(r'^new/', 'expenses.views.new', name='new_expense_url'),
	url(r'^create/', 'expenses.views.create', name='create_expense_url'),
	url(r'^edit/(\d+)', 'expenses.views.edit', name='edit_expense_url'),
	url(r'^update/(\d+)', 'expenses.views.update', name='update_expense_url'),
	url(r'^delete/(\d+)', 'expenses.views.destroy', name='delete_expense_url'),
)