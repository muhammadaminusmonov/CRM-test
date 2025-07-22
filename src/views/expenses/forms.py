# finance/forms.py
from django import forms
from finance.models import Expanses

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expanses
        fields = ['name', 'description', 'date', 'amount', 'status']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'name': 'Expense Name',
            'amount': 'Amount ($)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].widget = forms.HiddenInput()