# views.py in manager app
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from projects.models import Project
from django.http import JsonResponse
from django.contrib import messages
from datetime import datetime

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

@login_required
def assign(request):
    return render(request, 'manager/assign.html')


@login_required
def create_paper_project(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        type = request.POST.get('type', 'paper')
        status = request.POST.get('status')
        version = request.POST.get('version')
        abstract = request.POST.get('abstract')
        submission_date = request.POST.get('submission_date')
        file = request.FILES.get('file')

        project = Project.objects.create(
            title=title,
            type=type,
            status=status,
            version=version,
            abstract=abstract,
            file=file,
            submission_date=submission_date,
            created_by=request.user,
        )
        return JsonResponse({'message': 'Paper project created', 'project_id': project.id})


@login_required
def add_paper_project(request):
    if request.method == 'POST':
        title = request.POST.get('paperTitle')
        paper_type = request.POST.get('paperType')  # 'internal' or 'external'
        status = request.POST.get('paperStatus')    # e.g., 'draft', 'submitted'
        version = request.POST.get('currentVersion')
        lead_author = request.POST.get('leadAuthor')
        co_authors = request.POST.get('coAuthors')
        target_journal = request.POST.get('targetJournal')
        submission_date = request.POST.get('submissionDate')
        abstract = request.POST.get('paperAbstract')
        file = request.FILES.get('paperFile')

        try:
            submission_date = datetime.strptime(submission_date, '%Y-%m-%d') if submission_date else None

            project = Project.objects.create(
                title=title,
                description=abstract,
                type='paper',
                status=status,
                version=version,
                created_by=request.user,
                target_journal=target_journal,
                lead_author=lead_author,
                co_authors=co_authors,
                submission_date=submission_date,
                manuscript=file,
                paper_type=paper_type
            )
            messages.success(request, 'Paper project created successfully.')
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
def paper_tracking(request):
    internal_papers = Project.objects.filter(type='paper', paper_type='internal')
    external_papers = Project.objects.filter(type='paper', paper_type='external')
    return render(request, 'manager/manager_journals.html', {
        'internal_papers': internal_papers,
        'external_papers': external_papers,
    })