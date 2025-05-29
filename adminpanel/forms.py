from django import forms
from .models import SupervisorFeedback

class SupervisorFeedbackForm(forms.ModelForm):
    class Meta:
        model = SupervisorFeedback
        fields = ['comments', 'uploaded_file', 'status']
        widgets = {
            'comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'uploaded_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
