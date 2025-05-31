# models.py in projects app
from django.db import models
from django.conf import settings

class LearningContent(models.Model):
    title = models.CharField(max_length=200)
    type = models.CharField(max_length=50)
    platform = models.CharField(max_length=100, null=True, blank=True)
    platform_logo = models.URLField(null=True, blank=True)
    description = models.TextField()
    link = models.URLField()
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='learning_resources', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Template(models.Model):
    CATEGORY_CHOICES = [
        ('Book', 'Book Templates'),
        ('Research', 'Research Papers'),
        ('Software', 'Software Development'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    file = models.FileField(upload_to='templates/')
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='uploaded_templates', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

