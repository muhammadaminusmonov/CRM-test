from django import forms
from finance.models import TeacherSalary, StaffSalary, Expanses
from teacher.models import Teacher
from staff.models import Staff

class TeacherSalaryForm(forms.ModelForm):
    class Meta:
        model = TeacherSalary
        fields = ['teacher', 'month', 'salary', 'paid', 'paid_date']
        widgets = {
            'month': forms.DateInput(attrs={'type': 'month'}),
            'paid_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['teacher'].queryset = Teacher.objects.filter(status=1)  # Only active teachers

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
        self.fields['staff'].queryset = Staff.objects.filter(status=1)  # Only active staff

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expanses
        fields = ['name', 'description', 'date', 'amount', 'status']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }