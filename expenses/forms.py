from django import forms
from expenses.models import Expense

class ExpenseForm(forms.ModelForm):
	class Meta:
		model = Expense
