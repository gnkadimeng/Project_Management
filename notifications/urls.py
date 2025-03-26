from django.urls import path
from .views import notification_list, mark_as_read, delete_notification, get_new_notifications

urlpatterns = [
    path("", notification_list, name="notifications"),
    path('mark-as-read/<int:notification_id>/', mark_as_read, name='mark_as_read'),
    path('delete/<int:notification_id>/', delete_notification, name='delete_notification'),
    path('fetch/', get_new_notifications, name='get_new_notifications'),
]
