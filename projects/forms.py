# projects/forms.py
from django import forms
from .models import DailyTask, StudentProfile, Submission, FeedbackReply, Meeting, ChatMessage, Project, Assignment, TeamMember, Task


# forms.py
class DailyTaskForm(forms.ModelForm):
    class Meta:
        model = DailyTask
        fields = ['title']


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
        fields = ['name', 'description', 'project_type', 'due_date', 'status']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

class AssignmentForm(forms.ModelForm):
    team_member = forms.ModelChoiceField(
        queryset=TeamMember.objects.all(),  # ✅ this is the fix
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label="Select team member",  # ✅ Custom label
        
    )

    class Meta:
        model = Assignment
        fields = ['team_member', 'responsibility']
        
        widgets = {
            'responsibility': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
    def __init__(self, *args, **kwargs):
        project = kwargs.pop('project', None)
        super().__init__(*args, **kwargs)
        if project:
            self.fields['team_member'].queryset = TeamMember.objects.exclude(
                id__in=Assignment.objects.filter(project=project).values('team_member')
            )
        else:
            self.fields['team_member'].queryset = TeamMember.objects.all()


class FileUploadForm(forms.Form):
    file = forms.FileField()

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'priority', 'due_date', 'status']