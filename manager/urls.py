from django.urls import path
from . import views

urlpatterns = [
    path('manager_dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('manager_books/', views.manager_books, name='manager_books'),
    path('app_kanban/', views.app_kanban, name='app_kanban'),
    path('manager_journals/', views.manager_journals, name='manager_journals'),
    path('manager_ganttchart/', views.manager_ganttchart, name='manager_ganttchart'),
    path('manager_elearning/', views.manager_elearning, name='manager_elearning'),
    path('manager_templates/', views.manager_templates, name='manager_templates'),
    path('manager_kanban/', views.manager_kanban, name='manager_kanban'),
]