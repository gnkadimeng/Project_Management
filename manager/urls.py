from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('manager_dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('manager_books/', views.manager_books, name='manager_books'),
    path('app_kanban/', views.app_kanban, name='app_kanban'),
    path('manager_journals/', views.manager_journals, name='manager_journals'),
    path('manager_ganttchart/', views.manager_ganttchart, name='manager_ganttchart'),
    path('manager_elearning/', views.elearning_page, name='manager_elearning'),
    path('manager_templates/', views.templates_page, name='manager_templates'),
    path('manager_kanban/', views.manager_kanban, name='manager_kanban'),
    path('add-paper/', views.add_paper_project, name='add_paper_project'),
    path('papers/', views.paper_tracking, name='paper_tracking'),
    path('add-task/', views.add_task, name='add_task'),
    path('edit-task/<int:task_id>/', views.edit_task, name='edit_task'),
    path('update-task-status/<int:task_id>/', views.update_task_status, name='update_task_status'),
    path('assign/', views.assign_projects_view, name='assign_projects'),
    path('create_project/', views.create_project, name='create_project'),
    path('project_detail/<int:project_id>/', views.project_detail, name='project_detail'),
    path('elearning/add/', views.add_learning_resource, name='add_learning_resource'),
    path('templates/add/', views.add_template, name='add_template'),
    path('templates/<int:pk>/edit/', views.edit_template, name='edit_template'),
    path('templates/<int:pk>/delete/', views.delete_template, name='delete_template'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)