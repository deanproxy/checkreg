"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client
from django.utils import simplejson
from expenses.models import Balance, Expense


class ExpenseTest(TestCase):
	client = Client()
	def test_get_total(self):
		"""
		First test that we get a valid response even with an empty table.
		Then test that we get a valid response after we create a new balance.
		"""

		response = self.client.get('/expenses/total/')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response['Content-Type'], 'application/json')
		json = simplejson.loads(response.content)
		self.assertEqual(json['amount'], 0.0)

		Balance.objects.create(amount=100.0)
		response = self.client.get('/expenses/total/')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response['Content-Type'], 'application/json')
		json = simplejson.loads(response.content)
		self.assertEqual(json['amount'], 100.0)


	def test_create_expense(self):
		"""
		Test creating an expense
			- Should have created the expense properly in the db
			- Should have updated the Balance table
		"""

		response = self.client.post('/expenses/create/', {'description':'Hello', 'amount':'100.0', 'deposit':'true'})
		self.assertEqual(response.status_code, 201)

		expense = Expense.objects.get(pk=1)
		self.assertEqual(expense.description, 'Hello')
		self.assertEqual(expense.amount, 100.0)

		balance = Balance.objects.get(pk=1)
		self.assertEqual(balance.amount, 100.0)

		# Create an expense that removes money from the balance
		response = self.client.post('/expenses/create/', {'description':'Spend', 'amount':'50.0'})
		self.assertEqual(response.status_code, 201)

		expense = Expense.objects.get(pk=2)
		self.assertEqual(expense.description, 'Spend')
		self.assertEqual(expense.amount, -50.0)

		balance = Balance.objects.get(pk=1)
		self.assertEqual(balance.amount, 50.0)

		# Test that we return a 500 if we don't pass validations. Not including an amount should do this.
		response = self.client.post('/expenses/create/', {'description':'Invalid'})
		self.assertEqual(response.status_code, 500)


	def test_delete_expense(self):
		"""
		Create an expense and then delete it.
			- Should remove value from database
			- Should update Balance
			- Should 404 when item to delete isn't found
		"""

		Balance.objects.create(amount=200.0)
		expense = Expense.objects.create(description='Delete Me', amount=100.0)
		url = '/expenses/delete/%d' % expense.id
		response = self.client.post(url)
		self.assertEqual(response.status_code, 201)

		balance = Balance.objects.get(pk=1)
		self.assertEqual(balance.amount, 100.0)

		expense = Expense.objects.filter(description='Delete Me')
		self.assertEqual(len(expense), 0)

		response = self.client.post('/expenses/delete/22')
		self.assertEqual(response.status_code, 404)

	def test_update_expense(self):
		"""
		Create an expense and then update it.
			- Should update the expense in the db
			- Should update Balance
			- Should 404 when unknown object is requested for update
		"""

		Balance.objects.create(amount=100.0)
		expense = Expense.objects.create(description='Hello', amount=100.0)
		url = '/expenses/update/%d' % expense.id
		response = self.client.post(url, {'description':'Dean says hi', 'amount':'50.0'})
		self.assertEqual(response.status_code, 201)

		expense = Expense.objects.get(pk=1)
		balance = Balance.objects.get(pk=1)
		self.assertEqual(expense.description, 'Dean says hi')
		self.assertEqual(expense.amount, -50.0)
		self.assertEqual(balance.amount, -50.0)

		response = self.client.post('/expenses/update/55', {'description':'Invalid', 'amount':'22.0'})
		self.assertEqual(response.status_code, 404)

	def test_list_expenses(self):
		"""
		Create 35 expenses. Make sure we only get back 30.
		"""

		for i in range(0, 35):
			desc = 'Item %d' % i
			Expense.objects.create(description=desc, amount=100.0)

		response = self.client.get('/expenses/list/')
		expenses = response.context['expenses']
		self.assertEqual(len(expenses), 30)
		self.assertEqual(expenses[0].description, 'Item 34')
		self.assertEqual(expenses[29].description, 'Item 5')
		self.assertEqual(response.context['remaining'], 5)

	def test_more_expenses(self):
		"""
		Create 35 expenses. Set offset to 30 and make sure we get back
		the first 5 records created.
		"""

		for i in range(0, 35):
			desc = 'Item %d' % i
			Expense.objects.create(description=desc, amount=100.0)

		response = self.client.get('/expenses/more/?offset=30')
		expenses = response.context['expenses']
		self.assertEqual(response.context['remaining'], 0)
		self.assertEqual(len(expenses), 5)
		# Items are in reverse order, so we should get back the first 5 that were created.
		self.assertEqual(expenses[0].description, 'Item 4')
		self.assertEqual(expenses[4].description, 'Item 0')

	def test_edit_expense(self):
		"""
		Just make sure that we get a 404 back if an id of an expense that does not exist is passed
		"""

		response = self.client.get('/expenses/edit/22')
		self.assertEqual(response.status_code, 404)







