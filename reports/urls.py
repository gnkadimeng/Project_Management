from django.urls import path
from .views import report_dashboard, export_admin_report_csv

urlpatterns = [
    path("", report_dashboard, name="reports"),
    path('export/csv/', export_admin_report_csv, name='export_csv'),
]
