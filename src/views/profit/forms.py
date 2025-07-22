from django import forms
from finance.models import Profit, Payment, Cost, Expanses
from django.db.models import Sum
from django.template.defaulttags import register
import builtins
from datetime import date

@register.filter
def div(value, arg):
    try:
        return float(value) / float(arg)
    except (ValueError, ZeroDivisionError):
        return 0

@register.filter
def mul(value, arg):
    try:
        return float(value) * float(arg)
    except ValueError:
        return 0

@register.filter
def absolute(value):
    try:
        return builtins.abs(float(value))
    except ValueError:
        return 0

class ProfitForm(forms.ModelForm):
    class Meta:
        model = Profit
        fields = '__all__'
        widgets = {
            'month': forms.DateInput(attrs={'type': 'date'}),
            'gross_profit': forms.NumberInput(attrs={'step': '0.01'}),
            'profit': forms.NumberInput(attrs={'step': '0.01'}),
        }

class MonthSelectForm(forms.Form):
    month = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'month', 'class': 'form-control'}),
        input_formats=['%Y-%m'],
        initial=date.today().strftime('%Y-%m')
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'initial' in kwargs and 'month' in kwargs['initial']:
            selected_date = kwargs['initial']['month']
            if isinstance(selected_date, date):
                self.initial['month'] = selected_date.strftime('%Y-%m')