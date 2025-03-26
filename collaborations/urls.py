from django.urls import path
from .views import collaboration_overview, view_task, delete_comment, delete_file

urlpatterns = [
    path('', collaboration_overview, name='collaborations'),
    path('task/<int:task_id>/', view_task, name='view_task'),
    path('comment/delete/<int:comment_id>/', delete_comment, name='delete_comment'),
    path('file/delete/<int:file_id>/', delete_file, name='delete_file'),

]
