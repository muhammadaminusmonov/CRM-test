# staff/forms.py
from django import forms
from staff.models import Staff


class StaffForm(forms.ModelForm):
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('support', 'Support Staff'),
        ('accounting', 'Accounting'),
        ('hr', 'Human Resources'),
        ('maintenance', 'Maintenance'),
    ]

    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)

    class Meta:
        model = Staff
        fields = '__all__'
        widgets = {
            'born_date': forms.DateInput(attrs={'type': 'date'}),
            'join_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].choices = Staff.STATUS_CHOICES