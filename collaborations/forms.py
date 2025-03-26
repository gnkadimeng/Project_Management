from django import forms
from .models import Comment, FileUpload

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add your comment here...'}),
        }

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = FileUpload
        fields = ['file']
