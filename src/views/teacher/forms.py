# teachers/forms.py
from django import forms
from teacher.models import Teacher


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = '__all__'
        widgets = {
            'born_date': forms.DateInput(attrs={'type': 'date'}),
            'fixed_salary': forms.RadioSelect(choices=[(True, 'Fixed'), (False, 'Percentage')]),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['percentage'].required = False