from django.db import models
from django.contrib.auth.models import User
from tasks.models import Task
import re
from django.utils.html import mark_safe

class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def formatted_content(self):
        # Replace @username with highlighted span
        formatted = re.sub(r'@(\w+)', r'<span class="mention">@\1</span>', self.content)
        return mark_safe(formatted)  # Allows HTML rendering

    def __str__(self):
        return f"{self.user.username}: {self.content[:50]}"

class FileUpload(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="files")
    file = models.FileField(upload_to="uploads/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"File for {self.task.title}"
