# views.py in manager app
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from projects.models import Project, Task, Assignment
from projects.forms import ProjectForm, AssignmentForm, TaskForm
from .models import LearningContent, Template, Paper, Book, Chapter
from .forms import BookForm
from django.http import JsonResponse
from django.contrib import messages
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
import json
from users.models import CustomUser
from django.contrib.auth import get_user_model
from collections import defaultdict
from django.db.models import Q
import pandas as pd
from django.core.files.base import ContentFile
from django.views.decorators.http import require_POST

User = get_user_model()


@login_required
def manager_dashboard(request):
    return render(request, 'manager/manager_dashboard.html')

@login_required
def app_kanban(request):
    phases = ["UX/UI", "Architecture", "Frontend", "Backend", "Testing", "Deployment"]
    return render(request, 'manager/app_kanban.html', {'phases': phases})


@login_required
def manager_ganttchart(request):
    return render(request, 'manager/manager_ganttchart.html')

# @login_required
# def manager_elearning(request):
#     return render(request, 'manager/manager_elearning.html')

# @login_required
# def manager_templates(request):
#     return render(request, 'manager/manager_templates.html')

# @login_required
# def manager_kanban(request):
#     tasks = Task.objects.filter(created_by=request.user)
#     context = {
#         'tasks': tasks,
#     }
#     return render(request, 'manager/manager_kanban.html', context)


@login_required
def manager_kanban(request):
    status_labels = {
        'todo': 'To Do',
        'in_progress': 'In Progress',
        'review': 'Review',
        'done': 'Done',
    }
    statuses = list(status_labels.keys())
    priorities = ['Low', 'Medium', 'High']

    # Filter tasks created by this manager only
    tasks = Task.objects.filter(created_by=request.user)
    tasks_by_status = defaultdict(list)
    for task in tasks:
        tasks_by_status[task.status].append(task)

    context = {
        'statuses': statuses,
        'status_labels': status_labels,
        'priorities': priorities,
        'tasks_by_status': dict(tasks_by_status),
        'today': now().date(),
    }
    return render(request, 'manager/manager_kanban.html', context)

# @csrf_exempt
# @login_required
# def update_task_status(request, task_id):
#     if request.method == "POST":
#         task = get_object_or_404(Task, id=task_id, created_by=request.user)
#         new_status = request.POST.get('status')
#         if new_status in ['todo', 'in-progress', 'review', 'complete']:
#             task.status = new_status
#             task.save()
#             return JsonResponse({'success': True})
#     return JsonResponse({'success': False}, status=400)



# @login_required
# def create_paper_project(request):
#     if request.method == 'POST':
#         title = request.POST.get('title')
#         type = request.POST.get('type', 'paper')
#         status = request.POST.get('status')
#         version = request.POST.get('version')
#         abstract = request.POST.get('abstract')
#         submission_date = request.POST.get('submission_date')
#         file = request.FILES.get('file')

#         project = Project.objects.create(
#             title=title,
#             type=type,
#             status=status,
#             version=version,
#             abstract=abstract,
#             file=file,
#             submission_date=submission_date,
#             created_by=request.user,
#         )
#         return JsonResponse({'message': 'Paper project created', 'project_id': project.id})


# @login_required
# def add_paper_project(request):
#     if request.method == 'POST':
#         title = request.POST.get('paperTitle')
#         paper_type = request.POST.get('paperType')  # 'internal' or 'external'
#         status = request.POST.get('paperStatus')    # e.g., 'draft', 'submitted'
#         version = request.POST.get('currentVersion')
#         lead_author = request.POST.get('leadAuthor')
#         co_authors = request.POST.get('coAuthors')
#         target_journal = request.POST.get('targetJournal')
#         submission_date = request.POST.get('submissionDate')
#         abstract = request.POST.get('paperAbstract')
#         file = request.FILES.get('paperFile')

#         try:
#             submission_date = datetime.strptime(submission_date, '%Y-%m-%d') if submission_date else None

#             project = Project.objects.create(
#                 title=title,
#                 description=abstract,
#                 type='paper',
#                 status=status,
#                 version=version,
#                 created_by=request.user,
#                 target_journal=target_journal,
#                 lead_author=lead_author,
#                 co_authors=co_authors,
#                 submission_date=submission_date,
#                 manuscript=file,
#                 paper_type=paper_type
#             )
#             messages.success(request, 'Paper project created successfully.')
#             return JsonResponse({'success': True})
#         except Exception as e:
#             return JsonResponse({'success': False, 'error': str(e)})

#     return JsonResponse({'success': False, 'error': 'Invalid request method'})

# @login_required
# def paper_tracking(request):
#     internal_papers = Project.objects.filter(type='paper', paper_type='internal')
#     external_papers = Project.objects.filter(type='paper', paper_type='external')
#     return render(request, 'manager/manager_journals.html', {
#         'internal_papers': internal_papers,
#         'external_papers': external_papers,
#     })

@login_required
def assign_projects_view(request):
    projects = Project.objects.filter(created_by=request.user)
    selected_project = None
    assignments = None
    assignment_form = None
    eligible_users = get_user_model().objects.exclude(role='student')
    project_form = ProjectForm()  # ✅ Add this

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
        'project_form': project_form,  # ✅ Add this to context
    }
    return render(request, 'manager/assign.html', context)

@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user
            project.save()
            messages.success(request, 'Project created successfully!')
            return redirect('assign_projects')  # redirect back to assign view
    return redirect('assign_projects')


@login_required
def assign_team_member(request, project_id):
    project = get_object_or_404(Project, id=project_id, created_by=request.user)

    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.project = project
            assignment.save()
            messages.success(request, f"{assignment.team_member} assigned!")
            return redirect(f"{reverse('assign_projects')}?project_id={project.id}")
        else:
            messages.error(request, 'Assignment failed. Please check the form.')

            # reload assign.html manually with full context
            projects = Project.objects.filter(created_by=request.user)
            assignments = project.assignments.all()
            eligible_users = get_user_model().objects.exclude(role='student')
            project_form = ProjectForm()

            context = {
                'projects': projects,
                'project': project,
                'assignments': assignments,
                'assignment_form': form,  # the form with errors
                'eligible_users': eligible_users,
                'project_form': project_form,
            }
            return render(request, 'manager/assign.html', context)

    return redirect(f"{reverse('assign_projects')}?project_id={project.id}")

@login_required
def remove_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id, project__created_by=request.user)
    if request.method == 'POST':
        assignment.delete()
        messages.success(request, 'Team member removed.')
        return redirect('assign_projects', project_id=assignment.project.id)



@login_required
def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        priority = request.POST.get('priority')
        due_date = request.POST.get('due_date') or None
        status = request.POST.get('status')


        Task.objects.create(
            title=title,
            priority=priority,
            due_date=due_date,
            status=status,
            created_by=request.user,
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
        try:
            task = get_object_or_404(Task, id=task_id)
            data = json.loads(request.body)
            new_status = data.get('status')

            if new_status in ['todo', 'in_progress', 'review', 'done']:
                task.status = new_status
                task.save()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': 'Invalid status'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': 'Invalid method'}, status=405)

    
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

@login_required
def manager_journal(request):
    internal_papers = Paper.objects.filter(internal_external='internal')
    external_papers = Paper.objects.filter(internal_external='external')
    return render(request, 'manager/manager_journal.html', {
        'internal_papers': internal_papers,
        'external_papers': external_papers,
    })


@login_required
def add_paper(request):
    if request.method == 'POST':
        print("POST DATA:", request.POST.dict())  # ← Add this to debug

        status = request.POST.get('paperStatus')
        paper_type = request.POST.get('paperType')
        
        if not status or not paper_type:
            messages.error(request, "Missing required fields.")
            return redirect('manager_journal')

        Paper.objects.create(
            title=request.POST.get('paperTitle'),
            internal_external=paper_type,
            paper_type='journal' if 'journal' in (request.POST.get('targetJournal') or '').lower() else 'conference',
            status=status,
            version=request.POST.get('currentVersion'),
            lead_author=request.POST.get('leadAuthor'),
            co_authors=request.POST.get('coAuthors'),
            target_journal=request.POST.get('targetJournal'),
            submission_date=request.POST.get('submissionDate') or None,
            abstract=request.POST.get('paperAbstract'),
            manuscript=request.FILES.get('paperFile'),
            created_by=request.user,
        )

        messages.success(request, "Paper added successfully.")
        return redirect('manager_journal')

    
@login_required
def upload_excel_papers(request):
    if request.method == 'POST' and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']
        df = pd.read_excel(excel_file)

        for _, row in df.iterrows():
            Paper.objects.create(
                title=row.get('Title'),
                internal_external=row.get('Type', '').lower(),
                paper_type=row.get('Paper Type', 'journal').lower(),
                status=row.get('Status', 'draft').lower(),
                version=row.get('Version', '1.0'),
                lead_author=row.get('Lead Author', ''),
                co_authors=row.get('Co Authors', ''),
                target_journal=row.get('Target Journal', ''),
                submission_date=row.get('Submission Date'),
                abstract=row.get('Abstract', ''),
                created_by=request.user
            )

        messages.success(request, "Papers uploaded successfully from Excel.")
    return redirect('manager_journal')

@login_required
def edit_paper(request, paper_id):
    paper = get_object_or_404(Paper, id=paper_id)
    if request.method == 'POST':
        paper.title = request.POST.get('paperTitle')
        paper.status = request.POST.get('paperStatus')
        paper.version = request.POST.get('currentVersion')
        paper.lead_author = request.POST.get('leadAuthor')
        paper.co_authors = request.POST.get('coAuthors')
        paper.target_journal = request.POST.get('targetJournal')
        paper.submission_date = request.POST.get('submissionDate')
        paper.abstract = request.POST.get('paperAbstract')
        if request.FILES.get('paperFile'):
            paper.manuscript = request.FILES['paperFile']
        paper.save()
        messages.success(request, "Paper updated successfully.")
        return redirect('manager_journal')
    return render(request, 'manager/edit_paper.html', {'paper': paper})

@require_POST
@login_required
def delete_paper(request, paper_id):
    paper = get_object_or_404(Paper, id=paper_id)
    paper.delete()
    messages.success(request, "Paper deleted.")
    return redirect('manager_journal')

@require_POST
@login_required
def edit_paper_ajax(request, paper_id):
    paper = get_object_or_404(Paper, id=paper_id)

    paper.title = request.POST.get('paperTitle')
    paper.status = request.POST.get('paperStatus')
    paper.version = request.POST.get('currentVersion')
    paper.lead_author = request.POST.get('leadAuthor')
    paper.co_authors = request.POST.get('coAuthors')
    paper.target_journal = request.POST.get('targetJournal')
    paper.submission_date = request.POST.get('submissionDate') or None
    paper.abstract = request.POST.get('paperAbstract')

    if request.FILES.get('paperFile'):
        paper.manuscript = request.FILES['paperFile']

    paper.save()
    return JsonResponse({'success': True})

@login_required
def manager_book(request):
    books = Book.objects.all().order_by('-created_at')  # You can filter by user if needed
    return render(request, 'manager/manager_book.html', {'books': books})


@csrf_exempt
def add_book(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            book = Book.objects.create(
                title=data.get('title'),
                lead_author=data.get('lead_author'),
                due_date=data.get('due_date') or None,
                description=data.get('description'),
                total_chapters=data.get('total_chapters') or 0,
                completed_chapters=data.get('completed_chapters') or 0,
                publisher=data.get('publisher'),
                status=data.get('status')
            )
            return JsonResponse({'success': True, 'book_id': book.id})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request'})


@csrf_exempt
def edit_book(request, book_id):
    book = Book.objects.get(id=book_id)
    if request.method == 'POST':
        data = json.loads(request.body)
        form = BookForm(data, instance=book)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'message': 'Invalid method'})

@csrf_exempt
def delete_book(request, book_id):
    if request.method == 'POST':
        Book.objects.filter(id=book_id).delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'message': 'Invalid method'})


def get_chapters(request, book_id):
    chapters = Chapter.objects.filter(book_id=book_id).values(
        'chapter_number', 'title', 'author', 'editor', 'status', 'last_updated'
    )
    return JsonResponse({'chapters': list(chapters)})



@csrf_exempt
def add_chapter(request, book_id):
    if request.method == "POST":
        data = json.loads(request.body)
        chapter = Chapter.objects.create(
            book_id=book_id,
            chapter_number=data["chapter_number"],
            title=data["title"],
            author=data["author"],
            editor=data.get("editor", ""),
            status=data["status"]
        )
        return JsonResponse({"success": True, "id": chapter.id})
    return JsonResponse({"success": False, "error": "Invalid request method"})

@csrf_exempt
def edit_chapter(request, chapter_id):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            chapter = Chapter.objects.get(id=chapter_id)
            chapter.chapter_number = data["chapter_number"]
            chapter.title = data["title"]
            chapter.author = data["author"]
            chapter.editor = data.get("editor", "")
            chapter.status = data["status"]
            chapter.save()
            return JsonResponse({"success": True})
        except Chapter.DoesNotExist:
            return JsonResponse({"success": False, "error": "Chapter not found"})
    return JsonResponse({"success": False, "error": "Invalid request method"})

