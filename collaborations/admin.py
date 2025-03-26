from django.contrib import admin
from .models import Comment, FileUpload

admin.site.register(Comment)
admin.site.register(FileUpload)
