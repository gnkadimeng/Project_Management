from django import forms
from .models import Book
from projects.models import Project

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'description', 'status', 'due_date', 'lead_author', 'publisher', 'total_chapters', 'completed_chapters']

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'project_type', 'status']