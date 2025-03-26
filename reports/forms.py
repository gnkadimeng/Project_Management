from django import forms
from tasks.models import Task
from django.contrib.auth.models import User

class AdminTaskAssignForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'assigned_to', 'status', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'})
        }
