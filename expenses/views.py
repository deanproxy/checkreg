import logging
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils import simplejson
from expenses.forms import ExpenseForm
from expenses.models import Expense, Balance

def index(request):
	return render(request, 'expenses/index.html')

def total(request):
	""" Display the total """

	json = {'amount':0.0}
	try:
		balance = Balance.objects.get(pk=1)
	except:
		pass
	else:
		json['amount'] = balance.amount
	return HttpResponse(simplejson.dumps(json), mimetype='application/json')

def list(request):
	""" render the list page with 30 entries """

	expenses = Expense.objects.all().order_by('created_at').reverse()[0:29]
	total = Expense.objects.count()
	remaining = total - len(expenses)
	return render(request, 'expenses/list.html', {'expenses':expenses, 'total':total, 'remaining':remaining})

def more(request):
	""" sends back more expenses """

	offset = int(request.GET['offset']) or 0
	max = int(request.GET['max']) or 30
	total = Expense.objects.count()

	# REMEMBER: The way the slice works on a QuerySet is [start_pos:end_pos]
	expenses = Expense.objects.all().order_by('created_at').reverse()[offset:max + offset]
	remaining = total - (offset + len(expenses))

	return render(request, 'expenses/_list.html', {'expenses':expenses, 'total':total, 'remaining':remaining})

def new(request):
	return render(request, 'expenses/new.html')

def create(request):
	""" Create an expense. Update the current Balance. """

	status = 201
	form_data = request.POST.copy()
	# Make sure the amount reflects whether we're a deposit or not...
	if 'deposit' not in form_data:
		form_data['amount'] = -float(form_data['amount'])
	form = ExpenseForm(form_data)
	if form.is_valid():
		expense = form.save()
		try:
			balance = Balance.objects.get(pk=1)
		except Balance.DoesNotExist:
			# We're just now starting the app or something happened to the db, create the expense record.
			balance = Balance.objects.create(amount=0.0)

		balance.amount += expense.amount
		balance.save()
	else:
		status = 500
		logging.error(form.errors)
	return HttpResponse(status=status)

def edit(request, id):
	expense = get_object_or_404(Expense, pk=id)
	return render(request, 'expenses/edit.html', {'expense':expense})

def update(request, id):
	status = 201
	expense = get_object_or_404(Expense, pk=id)

	form_data = request.POST.copy()
	old_amount = expense.amount

	# Make sure the amount reflects whether we're a deposit or not...
	if 'deposit' not in form_data:
		form_data['amount'] = -float(form_data['amount'])
	form = ExpenseForm(form_data, instance=expense)
	if form.is_valid():
		new_expense = form.save()
		try:
			balance = Balance.objects.get(pk=1)
		except Balance.DoesNotExist:
			logging.error('Missing Balance record. What happened? Panic!')
			status = 500
		else:
			balance.amount -= old_amount
			balance.amount += new_expense.amount
			balance.save()
	else:
		logging.error(form.errors)
		status = 500
	return HttpResponse(status=status)


def destroy(request, id):
	""" Delete an expense. Update the current Balance. """

	response = 201
	expense = get_object_or_404(Expense, pk=id)
	try:
		# Make sure to update balance depending on the transaction type.
		balance = Balance.objects.get(pk=1)
		balance.amount -= expense.amount
		balance.save()
		expense.delete()
	except:
		response = 500
	return HttpResponse(status=response)

