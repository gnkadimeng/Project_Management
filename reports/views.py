from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from tasks.models import Task
from django.contrib.auth.models import User
import csv
from django.http import HttpResponse
from .forms import AdminTaskAssignForm


@login_required
def report_dashboard(request):
    tasks = Task.objects.all()

    # Filters (optional, reused by both views)
    user_id = request.GET.get('user')
    status = request.GET.get('status')
    due = request.GET.get('due')

    if user_id and user_id != 'all':
        tasks = tasks.filter(assigned_to__id=user_id)
    if status and status != 'all':
        tasks = tasks.filter(status=status)
    if due and due != '':
        tasks = tasks.filter(due_date=due)

    total = tasks.count()
    completed = tasks.filter(status='done').count()
    in_progress = tasks.filter(status='in_progress').count()
    todo = tasks.filter(status='todo').count()

    users = User.objects.all()

    # Admin View
    if request.user.is_staff:

        form = AdminTaskAssignForm()

        if request.method == 'POST':
            form = AdminTaskAssignForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Task assigned successfully.")
                return redirect('reports')

        # Full view of each user’s task completion
        user_data = []
        for user in users:
            user_tasks = Task.objects.filter(assigned_to=user)
            user_data.append({
                'name': user.username,
                'completed': user_tasks.filter(status='done').count(),
                'in_progress': user_tasks.filter(status='in_progress').count(),
                'todo': user_tasks.filter(status='todo').count(),
                'total': user_tasks.count(),
            })

        return render(request, "reports/admin_dashboard.html", {
            "user_data": user_data,
            "total": total,
            "completed": completed,
            "in_progress": in_progress,
            "todo": todo,
            "users": users,
            "selected_user": int(user_id) if user_id and user_id != 'all' else 'all',
            "selected_status": status or 'all',
            "selected_due": due or '',
        })

    # Regular User View
    return render(request, "reports/report_dashboard.html", {
        "tasks": tasks,
        "users": users,
        "total": total,
        "completed": completed,
        "in_progress": in_progress,
        "todo": todo,
        "selected_user": int(user_id) if user_id and user_id != 'all' else 'all',
        "selected_status": status or 'all',
        "selected_due": due or '',
    })


@login_required
def export_admin_report_csv(request):
    if not request.user.is_staff:
        return redirect('reports')

    # Create the HttpResponse object with CSV header
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="admin_team_report.csv"'

    writer = csv.writer(response)
    writer.writerow(['Username', 'Total Tasks', 'Completed', 'In Progress', 'To Do'])

    users = User.objects.all()
    for user in users:
        tasks = Task.objects.filter(assigned_to=user)
        writer.writerow([
            user.username,
            tasks.count(),
            tasks.filter(status='done').count(),
            tasks.filter(status='in_progress').count(),
            tasks.filter(status='todo').count()
        ])

    return response