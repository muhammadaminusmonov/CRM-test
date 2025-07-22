# classes/forms.py
from django import forms
from classes.models import Class


class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['title', 'cost_per_month', 'duration_per_lesson',
                  'length', 'description', 'status']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'status': forms.Select(choices=Class.STATUS_CHOICES),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['duration_per_lesson'].widget = forms.TimeInput(attrs={'type': 'time'})