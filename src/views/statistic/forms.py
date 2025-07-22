# forms.py
from django import forms
from classes.models import Class, Group, Attendance
from finance.models import Payment, Expanses, TeacherSalary, StaffSalary
from student.models import Student
from teacher.models import Teacher
from staff.models import Staff

# Add similar forms for other models as needed
class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = '__all__'
        widgets = {
            'start_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = '__all__'
        widgets = {
            'paid_at': forms.DateInput(attrs={'type': 'date'}),
        }