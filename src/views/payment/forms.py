# finance/forms.py
from django import forms
from finance.models import Payment
from student.models import Student
from classes.models import Group
from teacher.models import Teacher
from django.utils import timezone

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['student', 'paid_at', 'amount', 'paid_for_month', 'to_group', 'to_teacher']
        widgets = {
            'paid_at': forms.DateInput(attrs={'type': 'date'}),
            'paid_for_month': forms.DateInput(attrs={'type': 'month'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['student'].queryset = Student.objects.filter(status=1)  # Active students
        self.fields['to_group'].queryset = Group.objects.filter(status=1)  # Active groups
        self.fields['to_teacher'].queryset = Teacher.objects.filter(status=1)  # Active teachers