from django import forms
from finance.models import StaffSalary
from staff.models import Staff
import datetime


class StaffSalaryForm(forms.ModelForm):
    class Meta:
        model = StaffSalary
        fields = ['staff', 'month', 'salary', 'paid', 'paid_date']
        widgets = {
            'month': forms.DateInput(attrs={'type': 'month'}),
            'paid_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['staff'].queryset = Staff.objects.all()
        self.fields['paid_date'].required = False


class SalaryFilterForm(forms.Form):
    MONTH_CHOICES = [
        ('all', 'All Months'),
        ('1', 'January'), ('2', 'February'), ('3', 'March'),
        ('4', 'April'), ('5', 'May'), ('6', 'June'),
        ('7', 'July'), ('8', 'August'), ('9', 'September'),
        ('10', 'October'), ('11', 'November'), ('12', 'December')
    ]

    STATUS_CHOICES = [
        ('all', 'All Status'),
        ('paid', 'Paid'),
        ('unpaid', 'Unpaid'),
        ('partial', 'Partial')
    ]

    search = forms.CharField(required=False)
    month = forms.ChoiceField(choices=MONTH_CHOICES, required=False)
    year = forms.IntegerField(
        min_value=2020,
        max_value=2030,
        initial=datetime.datetime.now().year
    )
    status = forms.ChoiceField(choices=STATUS_CHOICES, required=False)