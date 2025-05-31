# views.py in manager app
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from projects.models import Project, Task
from django.http import JsonResponse
from django.contrib import messages
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
import json
from users.models import CustomUser
from projects.forms import ProjectForm, AssignmentForm
from django.contrib.auth import get_user_model
from collections import defaultdict
from manager.models import LearningContent, Template
from django.db.models import Q


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

# @login_required
# def manager_kanban(request):
#     tasks = Task.objects.filter(created_by=request.user)
#     context = {
#         'tasks': tasks,
#     }
#     return render(request, 'manager/manager_kanban.html', context)


@login_required
def manager_kanban(request):
    statuses = ['To Do', 'In Progress', 'Review', 'Complete']
    priorities = ['Low', 'Medium', 'High']
    eligible_users = CustomUser.objects.filter(role__in=['staff', 'manager'])

    # Group tasks by project, then by status
    projects_tasks = {}
    all_projects = Project.objects.all()

    for project in all_projects:
        tasks = Task.objects.filter(project=project)
        status_dict = defaultdict(list)
        for task in tasks:
            status_dict[task.status].append(task)
        projects_tasks[project] = status_dict

    context = {
        'all_projects': all_projects,  # used in the HTML
        'projects_tasks': projects_tasks,  # used in the HTML
        'statuses': statuses,
        'priorities': priorities,
        'eligible_users': eligible_users,
        'today': now().date(),
    }
    return render(request, 'manager/manager_kanban.html', context)

@csrf_exempt
@login_required
def update_task_status(request, task_id):
    if request.method == "POST":
        task = get_object_or_404(Task, id=task_id, created_by=request.user)
        new_status = request.POST.get('status')
        if new_status in ['todo', 'in-progress', 'review', 'complete']:
            task.status = new_status
            task.save()
            return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)



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

@login_required
def assign_projects_view(request):
    projects = Project.objects.filter(created_by=request.user)
    selected_project = None
    assignments = None
    assignment_form = None
    eligible_users = get_user_model().objects.exclude(role='student')

    project_id = request.GET.get('project_id')
    if project_id:
        selected_project = get_object_or_404(Project, id=project_id)
        assignments = selected_project.assignments.all()
        assignment_form = AssignmentForm()

    context = {
        'projects': projects,
        'project': selected_project,
        'assignments': assignments,
        'assignment_form': assignment_form,
        'eligible_users': eligible_users,
    }
    return render(request, 'manager/assign.html', context)

def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user
            project.save()
            messages.success(request, 'Project created successfully!')
            return redirect('project_detail', project_id=project.id)
    else:
        form = ProjectForm()
   
    return render(request, 'manager/create_project.html', {'form': form})

@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id, created_by=request.user)

    if request.method == 'POST':
        assignment_form = AssignmentForm(request.POST)
        if assignment_form.is_valid():
            assignment = assignment_form.save(commit=False)
            assignment.project = project
            assignment.save()
            messages.success(request, f'{assignment.team_member} assigned!')
            return redirect(f"{reverse('assign_projects')}?project_id={project.id}")

    return redirect(f"{reverse('assign_projects')}?project_id={project.id}")


@login_required
def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        priority = request.POST.get('priority')
        due_date = request.POST.get('due_date') or None
        status = request.POST.get('status')
        assigned_id = request.POST.get('assigned_to')
        assigned_user = get_user_model().objects.get(id=assigned_id)

        Task.objects.create(
            title=title,
            priority=priority,
            due_date=due_date,
            status=status,
            assigned_to=request.user,  # you can customize this later
        )
    return redirect('manager_kanban')


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.priority = request.POST.get('priority')
        task.due_date = request.POST.get('due_date') or None
        task.save()
        return redirect('manager_kanban')


@csrf_exempt
@login_required
def update_task_status(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id)
        data = json.loads(request.body)
        task.status = data.get('status')
        task.save()
        return JsonResponse({'success': True})
    
@login_required
def add_learning_resource(request):
    if request.method == 'POST' and request.user.role == 'manager':
        title = request.POST['title']
        type_ = request.POST['type']
        platform = request.POST['platform']
        platform_logo = request.POST['platform_logo']
        description = request.POST['description']
        link = request.POST['link']

        LearningContent.objects.create(
            title=title,
            type=type_,
            platform=platform,
            platform_logo=platform_logo,
            description=description,
            link=link,
            added_by=request.user
        )
        messages.success(request, 'Resource added successfully.')
    return redirect('manager_elearning')

@login_required
def elearning_page(request):
    resource_type = request.GET.get('type', '').strip()
    search_query = request.GET.get('search', '').strip()


    resources = LearningContent.objects.all()

    if resource_type and resource_type.lower() != "all":
        resources = resources.filter(type__icontains=resource_type)

    if search_query:
        resources = resources.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    resources = resources.order_by('-created_at')
    distinct_types = LearningContent.objects.values_list('type', flat=True).distinct()


    print("Type:", resource_type)
    print("Search:", search_query)
    print("Final count:", resources.count())


    return render(request, 'manager/manager_elearning.html', {
        'resources': resources,
        'selected_type': resource_type or 'All',
        'search_query': search_query,
        'resource_types': distinct_types,  # NEW!
    })


@login_required
def templates_page(request):
    search_query = request.GET.get('search', '').strip()

    book_templates = Template.objects.filter(category='Book')
    research_templates = Template.objects.filter(category='Research')
    software_templates = Template.objects.filter(category='Software')

    if search_query:
        book_templates = book_templates.filter(
            Q(title__icontains=search_query) | Q(description__icontains=search_query)
        )
        research_templates = research_templates.filter(
            Q(title__icontains=search_query) | Q(description__icontains=search_query)
        )
        software_templates = software_templates.filter(
            Q(title__icontains=search_query) | Q(description__icontains=search_query)
        )

    categories = {
        'Book Templates': book_templates,
        'Research Papers': research_templates,
        'Software Development': software_templates,
    }

    return render(request, 'manager/manager_templates.html', {
        'template_categories': categories,
        'search_query': search_query
    })



@login_required
def add_template(request):
    if request.method == 'POST' and request.user.role == 'manager':
        title = request.POST['title']
        description = request.POST['description']
        category = request.POST['category']
        file = request.FILES['file']

        if file:
            Template.objects.create(
                title=title,
                description=description,
                category=category,
                file=file,
                uploaded_by=request.user
            )
    return redirect('manager_templates')

@login_required
def edit_template(request, pk):
    template = get_object_or_404(Template, pk=pk, uploaded_by=request.user)
    if request.method == 'POST':
        template.title = request.POST['title']
        template.description = request.POST['description']
        template.category = request.POST['category']
        if 'file' in request.FILES:
            template.file = request.FILES['file']
        template.save()
        return redirect('manager_templates')
    return render(request, 'manager/edit_template.html', {'template': template})


@login_required
def delete_template(request, pk):
    template = get_object_or_404(Template, pk=pk, uploaded_by=request.user)
    if request.method == 'POST':
        template.delete()
    return redirect('manager_templates')

