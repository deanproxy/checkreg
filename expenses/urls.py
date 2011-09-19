from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
	url(r'^list/', 'expenses.views.list', name='list_expense_url'),
	url(r'^total/', 'expenses.views.total', name='total_url'),
	url(r'^create/', 'expenses.views.create', name='create_expense_url'),
	url(r'^delete/(\d+)', 'expenses.views.destroy', name='delete_expense_url'),
)