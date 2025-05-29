from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('staff_kanban/', views.staff_kanban, name='staff_kanban'),
    path('journals/', views.journals_view, name='journals'),
    path('books/', views.books_view, name='books'),
    path('projects_review/', views.projects_review, name='projects_review'),
    path('ganttchart/', views.ganttchart, name='ganttchart'),
    path('task/done/<int:task_id>/', views.mark_task_done, name='mark_task_done'),
    path('task/delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('elearning/', views.elearning, name='elearning'), 
    path('templates/', views.templates, name='templates'), 
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'), 
    path('submit-document/', views.submit_document, name='submit_document'),
    path('submit-feedback-reply/<int:submission_id>/', views.submit_feedback_reply, name='submit_feedback_reply'),
    path('notification/read/<int:notif_id>/', views.mark_notification_read, name='mark_notification_read'),
    path('submit-meeting/', views.submit_meeting_request, name='submit_meeting'),
    path('send-chat/', views.send_chat_message, name='send_chat'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)