from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def manager_dashboard(request):
    return render(request, 'manager/manager_dashboard.html')

@login_required
def manager_books(request):
    return render(request, 'manager/manager_books.html')

@login_required
def app_kanban(request):
    phases = ["UX/UI", "Architecture", "Frontend", "Backend", "Testing", "Deployment"]
    return render(request, 'manager/app_kanban.html', {'phases': phases})

@login_required
def manager_journals(request):
    return render(request, 'manager/manager_journals.html')

@login_required
def manager_ganttchart(request):
    return render(request, 'manager/manager_ganttchart.html')

@login_required
def manager_elearning(request):
    return render(request, 'manager/manager_elearning.html')

@login_required
def manager_templates(request):
    return render(request, 'manager/manager_templates.html')

@login_required
def manager_kanban(request):
    return render(request, 'manager/manager_kanban.html')