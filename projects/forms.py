# projects/forms.py
from django import forms
from .models import DailyTask, StudentProfile, Submission, FeedbackReply, Meeting, ChatMessage, Project, Assignment, TeamMember

class DailyTaskForm(forms.ModelForm):
    class Meta:
        model = DailyTask
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'New task...',
                'class': 'form-control',
            }),
        }

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['program', 'co_supervisor', 'research_title', 'year']
        widgets = {
            'program': forms.Select(attrs={'class': 'form-select'}),
            'co_supervisor': forms.TextInput(attrs={'class': 'form-control'}),
            'research_title': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.TextInput(attrs={'class': 'form-control'}),
        }

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['document_type', 'title', 'file', 'notes']
        widgets = {
            'document_type': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class FeedbackReplyForm(forms.ModelForm):
    class Meta:
        model = FeedbackReply
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Write a reply...'}),
        }

class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = ['date', 'time', 'duration', 'purpose', 'mode']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'purpose': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'mode': forms.Select(attrs={'class': 'form-select'}),
        }

class ChatForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ['message']
        widgets = {
            'message': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type your message...'})
        }


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'project_type']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['team_member', 'responsibility']
        widgets = {
            'responsibility': forms.Textarea(attrs={'rows': 3}),
        }
   
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['team_member'].queryset = TeamMember.objects.all()
        self.fields['team_member'].label_from_instance = lambda obj: obj.full_name


