from django import forms
from classes.models import Group
from student.models import Student
from teacher.models import Teacher
from classes.models import Class

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'teacher', 'classes', 'start_at', 'end_at', 'lesson_per_week', 'status']
        widgets = {
            'start_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'lesson_per_week': forms.NumberInput(attrs={'min': 1, 'max': 7}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['teacher'].queryset = Teacher.objects.filter(status=1)  # Only active teachers
        self.fields['classes'].queryset = Class.objects.filter(status=1)  # Only active classes

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'join_date', 'status']
        widgets = {
            'join_date': forms.DateInput(attrs={'type': 'date'}),
        }