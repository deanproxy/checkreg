import logging
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils import simplejson
from expenses.forms import ExpenseForm
from expenses.models import Expense, Balance

def index(request):
	return render(request, 'index.html')

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
	""" Get the current expenses and format them into json. An offset and max may be provided """

	offset = int(request.GET['offset']) or 0
	max = int(request.GET['max']) or 30
	total = Expense.objects.count()
	json = {'total':total, 'expenses':[]}

	# REMEMBER: The way the slice works on a QuerySet is [start_pos:end_pos]
	expenses = Expense.objects.all().order_by('created_at').reverse()[offset:max + offset]
	for expense in expenses:
		json['expenses'].append({
			'id': expense.id,
			'createdAt': expense.created_at.strftime("%b %d, %Y"),
			'description': expense.description,
			'amount': expense.amount,
			'deposit': expense.deposit
		})
	return HttpResponse(simplejson.dumps(json), mimetype='application/json')

def create(request):
	""" Create an expense. Update the current Balance. """

	status = 201
	form = ExpenseForm(request.POST)
	if form.is_valid():
		expense = form.save()
		try:
			balance = Balance.objects.get(pk=1)
		except Balance.DoesNotExist:
			# We're just now starting the app or something happen to the db, create the expense record.
			balance = Balance.objects.create(amount=0.0)

		# Update the total amount depending on what type of transaction
		if expense.deposit:
			balance.amount += expense.amount
		else:
			balance.amount -= expense.amount
		balance.save()
	else:
		status = 500
		logging.error(form.errors)
	return HttpResponse(status=status)

def destroy(request, id):
	""" Delete an expense. Update the current Balance. """

	response = 201
	expense = get_object_or_404(Expense, pk=id)
	try:
		# Make sure to update balance depending on the transaction type.
		balance = Balance.objects.get(pk=1)
		if expense.deposit:
			balance.amount -= expense.amount
		else:
			balance.amount += expense.amount
		balance.save()
		expense.delete()
	except:
		response = 500
	return HttpResponse(status=response)

