from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('manager_dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('manager_book/', views.manager_book, name='manager_book'),
    path('app_kanban/', views.app_kanban, name='app_kanban'),
    path('manager_journal/', views.manager_journal, name='manager_journal'),
    path('manager_ganttchart/', views.manager_ganttchart, name='manager_ganttchart'),
    path('manager_elearning/', views.elearning_page, name='manager_elearning'),
    path('manager_templates/', views.templates_page, name='manager_templates'),
    path('manager_kanban/', views.manager_kanban, name='manager_kanban'),
    # path('add-paper/', views.add_paper_project, name='add_paper_project'),
    # path('papers/', views.paper_tracking, name='paper_tracking'),
    path('add-task/', views.add_task, name='add_task'),
    path('edit-task/<int:task_id>/', views.edit_task, name='edit_task'),
    path('update-task-status/<int:task_id>/', views.update_task_status, name='update_task_status'),
    path('assign/', views.assign_projects_view, name='assign_projects'),
    path('create_project/', views.create_project, name='create_project'),
    path('assign/team/<int:project_id>/', views.assign_team_member, name='assign_team_member'),
    path('elearning/add/', views.add_learning_resource, name='add_learning_resource'),
    path('templates/add/', views.add_template, name='add_template'),
    path('templates/<int:pk>/edit/', views.edit_template, name='edit_template'),
    path('templates/<int:pk>/delete/', views.delete_template, name='delete_template'),
    path('add-paper/', views.add_paper, name='add_paper'),
    path('upload-excel/', views.upload_excel_papers, name='upload_excel_papers'),
    path('edit/<int:paper_id>/', views.edit_paper, name='edit_paper'),
    path('delete/<int:paper_id>/', views.delete_paper, name='delete_paper'),
    path('edit-ajax/<int:paper_id>/', views.edit_paper_ajax, name='edit_paper_ajax'),
    path('add-book/', views.add_book, name='add_book'),
    path('edit-book/<int:book_id>/', views.edit_book, name='edit_book'),
    path('delete-book/<int:book_id>/', views.delete_book, name='delete_book'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)