from django.contrib import admin
from .models import LearningContent, Template, Paper, Book, Chapter

# Register your models here.
admin.site.register(LearningContent)
admin.site.register(Template)
admin.site.register(Paper)
admin.site.register(Book)
admin.site.register(Chapter)
