from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Notification
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string

@login_required
def notification_list(request):
    all_notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    mention_notifications = all_notifications.filter(message__icontains="mentioned")
    regular_notifications = all_notifications.exclude(id__in=mention_notifications)

    return render(request, 'notifications/notifications.html', {
        'notifications': regular_notifications,
        'mentions': mention_notifications
    })


@login_required
def mark_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return redirect('notifications')

@login_required
def delete_notification(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.delete()
    return redirect('notifications')

def get_new_notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    html = render_to_string('notifications/partials/notification_list.html', {'notifications': notifications})
    return JsonResponse({'html': html})


