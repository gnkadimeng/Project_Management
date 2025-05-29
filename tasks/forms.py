from django import forms
from .models import Task, FileUpload

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status']

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = FileUpload
        fields = ['task', 'file_path']
        widgets = {
            'task': forms.HiddenInput()
        }
