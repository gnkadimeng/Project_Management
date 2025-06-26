from django.urls import path
from . import views

urlpatterns = [
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin_book/', views.admin_book, name='admin_book'),
    path('app_kanban/', views.app_kanban, name='app_kanban'),
    path('admin_journal/', views.admin_journal, name='admin_journal'),
    path('admin_ganttchart/', views.admin_ganttchart, name='admin_ganttchart'),
    path('overview/', views.overview, name='overview'),
    path('finance/', views.finance, name='finance'),
    path('admin_kanban/', views.admin_kanban, name='admin_kanban'),
    path('supervisor_dashboard/', views.supervisor_dashboard, name='supervisor_dashboard'),
    path('finance/add-cost-centre/', views.add_cost_centre, name='add_cost_centre'),
    path('finance/expenditures/<int:cost_centre_id>/', views.get_expenditures, name='get_expenditures'),
    path('feedback/<int:submission_id>/', views.provide_feedback, name='provide_feedback'),
    path('finance/add-expenditure/', views.add_expenditure, name='add_expenditure'),
    path('finance/delete-cost-centre/<int:pk>/', views.delete_cost_centre, name='delete_cost_centre'),
    path('finance/edit-cost-centre/<int:pk>/', views.edit_cost_centre, name='edit_cost_centre'),
    path('finance/edit-expenditure/<int:pk>/', views.edit_expenditure, name='edit_expenditure'),
    path('finance/delete-expenditure/<int:pk>/', views.delete_expenditure, name='delete_expenditure'),
    path('admin/user-kanban/<int:user_id>/', views.admin_user_kanban, name='admin_user_kanban'),
    path('assign-project/', views.assign_project, name='assign_project'),
    path('api/gantt-data/', views.gantt_data_api, name='gantt_data_api'),
    path('admin/project-tasks/<str:project_name>/', views.project_task_detail, name='project_task_detail'),
    path('admin/update-task-progress/<int:task_id>/', views.update_task_progress, name='update_task_progress'),

]
