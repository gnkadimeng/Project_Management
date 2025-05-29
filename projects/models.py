from django.db import models
from django.conf import settings
from adminpanel.models import SupervisorProfile

# Create your models here.
class Project(models.Model):
    PROJECT_TYPE_CHOICES = [
        ('paper', 'Paper'),
        ('book', 'Book'),
        ('software', 'Software'),
     
    ]
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=50, choices=PROJECT_TYPE_CHOICES)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_projects')
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=50, default='active')

    def __str__(self):
        return self.name
    
class DailyTask(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class StudentProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    program = models.CharField(max_length=100)
    co_supervisor = models.CharField(max_length=100, blank=True, null=True)
    research_title = models.CharField(max_length=255)
    year = models.CharField(max_length=50) 
    supervisor = models.ForeignKey(SupervisorProfile, on_delete=models.SET_NULL, null=True, related_name='students')
    
    def __str__(self):
        return self.user.get_full_name()
    

class Submission(models.Model):
    DOCUMENT_TYPES = [
        ('Paper', 'Paper'),
         ('Chapter', 'Chapter'),
        ('Proposal', 'Proposal'),
        ('Thesis', 'Thesis'),
        ('Report', 'Report'),
        ('Other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('Pending Review', 'Pending Review'),
        ('Approved', 'Approved'),
        ('Feedback Provided', 'Feedback Provided'),
        ('Rejected', 'Rejected'),
    ]

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='submissions/')
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Pending Review')
    created_at = models.DateTimeField(auto_now_add=True)
    feedback_text = models.TextField(blank=True, null=True)
    feedback_file = models.FileField(upload_to='feedback/', blank=True, null=True)
    version_number = models.IntegerField(default=1)


    def __str__(self):
        return f"{self.student.get_full_name()} - {self.title}"
    
class FeedbackReply(models.Model):
    submission = models.ForeignKey('Submission', on_delete=models.CASCADE, related_name='replies')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.get_full_name()} replied on {self.created_at.strftime('%Y-%m-%d')}"

class Notification(models.Model):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.recipient.username} - {self.title}"
    
class Meeting(models.Model):
    MODE_CHOICES = [
        ('In-person', 'In-person'),
        ('Virtual', 'Virtual'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    duration = models.IntegerField(help_text="Duration in minutes")
    purpose = models.TextField()
    mode = models.CharField(max_length=20, choices=MODE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.get_full_name()} – {self.date} @ {self.time}"

class ChatMessage(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    submission = models.ForeignKey('Submission', on_delete=models.CASCADE, related_name='chat_messages', null=True, blank=True)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.get_full_name()} – {self.timestamp.strftime('%H:%M')}"

