from django import forms
from expenses.models import Expense

class ExpenseForm(forms.ModelForm):

	def save(self, commit=True):
		"""
		Make sure amount is negative if this is not a deposit
		"""

		expense = super(ExpenseForm, self).save(commit=False)
		if 'deposit' not in self.data or self.data['deposit'] == 'false':
			expense.amount = -expense.amount
		expense.save()
		return expense

	class Meta:
		model = Expense
