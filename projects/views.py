# projects/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import DailyTask, StudentProfile, Submission, Notification, Meeting, ChatMessage, Project, Assignment, TeamMember, Task
from users.models import CustomUser
from .forms import DailyTaskForm, StudentProfileForm, SubmissionForm, FeedbackReplyForm, MeetingForm, ChatForm, ProjectForm, AssignmentForm
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import date
from django.utils.timezone import now
from django.contrib import messages
from django.urls import reverse
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.contrib.auth import get_user_model
from manager.models import LearningContent, Template
from django.db.models import Q



# @login_required
# def dashboard(request):
#     user = request.user
#     form = TaskForm()

#     if request.method == 'POST':
#         form = TaskForm(request.POST)
#         if form.is_valid():
#             new_task = form.save(commit=False)
#             new_task.assigned_to = user
#             new_task.save()
#             return redirect('dashboard')

#     # Get user's tasks
#     my_tasks_today = Task.objects.filter(assigned_to=user).order_by('-created_at')
#     completed = Task.objects.filter(assigned_to=user, status='done').count()
#     in_progress = Task.objects.filter(assigned_to=user, status='in_progress').count()
#     total_projects = my_tasks_today.count()

#     context = {
#         'form': form,
#         'my_tasks_today': my_tasks_today,
#         'completed': completed,
#         'in_progress': in_progress,
#         'total_projects': total_projects,
#     }

#     return render(request, 'projects/dashboard.html', context)


@login_required
def dashboard(request):
    form = DailyTaskForm()
    tasks = DailyTask.objects.filter(user=request.user).order_by('-created_at')

    upload_form = FileUploadForm()

    if request.method == 'POST':
        form = DailyTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('dashboard')

    return render(request, 'projects/dashboard.html', {
        'form': form,
        'daily_tasks': tasks,
        'upload_form': upload_form
    })


@login_required
def mark_task_done(request, task_id):
    task = get_object_or_404(DailyTask, id=task_id, user=request.user)
    task.is_done = True
    task.save()
    return redirect('dashboard')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(DailyTask, id=task_id, user=request.user)
    task.delete()
    return redirect('dashboard')

@login_required
def staff_kanban(request):
    team_member = TeamMember.objects.filter(user=request.user).first()

    tasks = Task.objects.filter(assigned_to=request.user)
    todo_tasks = tasks.filter(status='To Do')
    in_progress_tasks = tasks.filter(status='In Progress')
    review_tasks = tasks.filter(status='Review')
    done_tasks = tasks.filter(status='Done')

    assignments = Assignment.objects.filter(team_member=team_member) if team_member else []

    context = {
        'assignments': assignments,
        'todo_tasks': todo_tasks,
        'in_progress_tasks': in_progress_tasks,
        'review_tasks': review_tasks,
        'done_tasks': done_tasks,
    }
    return render(request, 'projects/staff_kanban.html', context)



@login_required
def staff_create_task(request):
    if request.method == 'POST':
        title = request.POST['title']
        status = request.POST['status']
        task_type = request.POST.get('task_type')
        priority = request.POST.get('priority')
        due_date_str = request.POST.get('due_date')

        # Convert due_date to a valid date or None
        due_date = None
        if due_date_str:
            try:
                due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
            except ValueError:
                due_date = None  # fallback if date is badly formatted

        # Create the task
        Task.objects.create(
            title=title,
            status=status,
            task_type=task_type,
            priority=priority,
            due_date=due_date,
            assigned_to=request.user,
            project=None  # optional: handle this based on your logic
        )
    return redirect('staff_kanban')

@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, assigned_to=request.user)

    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.status = request.POST.get('status')
        task.task_type = request.POST.get('task_type')
        task.priority = request.POST.get('priority')
        task.due_date = request.POST.get('due_date') or None  # handle empty date field
        task.save()
        return redirect('staff_kanban')  # Replace with your actual task board URL name

    # If someone tries GET on this view directly
    return redirect('staff_kanban')

@csrf_exempt
@login_required
def update_task_status(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id, assigned_to=request.user)
        data = json.loads(request.body)
        task.status = data.get('status')
        task.save()
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Invalid method'}, status=400)


@csrf_exempt
def update_task_status(request, task_id):
    if request.method == 'POST':
        try:
            task = Task.objects.get(id=task_id)
            data = json.loads(request.body)
            new_status = data.get("status")
            if new_status in ["To Do", "In Progress", "Done"]:
                task.status = new_status
                task.save()
                return JsonResponse({"success": True})
            else:
                return JsonResponse({"error": "Invalid status"}, status=400)
        except Task.DoesNotExist:
            return JsonResponse({"error": "Task not found"}, status=404)
    return JsonResponse({"error": "Invalid request"}, status=400)


@login_required
def projects_review(request):
    return render(request, 'projects/projects_review.html')

@login_required
def ganttchart(request):
    if request.user.is_superuser or request.user.role == 'admin':
        tasks = Task.objects.all()
    else:
        tasks = Task.objects.filter(assigned_to=request.user)

    return render(request, 'projects/ganttchart.html', {'tasks': tasks})


def is_student(user):
    return user.role == 'student'

@login_required
@user_passes_test(is_student)
def student_dashboard(request):
    profile, created = StudentProfile.objects.get_or_create(user=request.user)

    # Handle profile form
    if request.method == 'POST' and 'update_profile' in request.POST:
        form = StudentProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            full_name = request.POST.get('name', '').strip()
            if full_name:
                parts = full_name.split()
                request.user.first_name = parts[0]
                request.user.last_name = ' '.join(parts[1:]) if len(parts) > 1 else ''
                request.user.save()
            return redirect('student_dashboard')
    else:
        form = StudentProfileForm(instance=profile)

    # Load submissions
    submissions = Submission.objects.filter(student=request.user).order_by('-created_at')
     # Filter feedback-provided submissions
    feedback_submissions = submissions.filter(status='Feedback Provided')

    # Submission form for modal
    submission_form = SubmissionForm()

    # Notifications
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    unread_count = notifications.filter(is_read=False).count()

    #Meeting form
    meetings = Meeting.objects.filter(student=request.user).order_by('-date')
    meeting_form = MeetingForm()

    chat_messages = ChatMessage.objects.filter(sender=request.user).order_by('timestamp')
    chat_form = ChatForm()

    context = {
        'student': {
            'name': request.user.get_full_name(),
            'program': profile.program,
            'co_supervisor': profile.co_supervisor,
            'research_title': profile.research_title,
            'year': profile.year,
            'supervisor': "Prof. Arnesh Telukdarie",
            'progress': 65
        },
        'user': request.user,
        'form': form,
        'submissions': submissions,
        'submission_form': submission_form,
    }

        # Add feedback submissions to context
    context.update({
        'feedback_submissions': feedback_submissions,
    })

    context.update({
        'notifications': notifications,
        'unread_notification_count': unread_count
    })

    context.update({
    'meetings': meetings,
    'meeting_form': meeting_form,
    })

    context.update({
    'chat_messages': chat_messages,
    'chat_form': chat_form,
    })

    return render(request, 'projects/student_dashboard.html', context)

@login_required
@user_passes_test(is_student)
def submit_document(request):
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            # Assign version based on existing submissions
            existing = Submission.objects.filter(student=request.user, title=form.cleaned_data['title']).order_by('-version_number').first()
            version = existing.version_number + 1 if existing else 1

            submission = form.save(commit=False)
            submission.student = request.user
            submission.version_number = version
            submission.save()

    return redirect('student_dashboard')


@login_required
@user_passes_test(is_student)
def submit_feedback_reply(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id, student=request.user)
    if request.method == 'POST':
        form = FeedbackReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.submission = submission
            reply.student = request.user
            reply.save()
    return redirect('student_dashboard')

@login_required
@user_passes_test(is_student)
def mark_notification_read(request, notif_id):
    notif = get_object_or_404(Notification, id=notif_id, recipient=request.user)
    notif.is_read = True
    notif.save()
    return redirect('student_dashboard')

@login_required
@user_passes_test(is_student)
def submit_meeting_request(request):
    if request.method == 'POST':
        form = MeetingForm(request.POST)
        if form.is_valid():
            meeting = form.save(commit=False)
            meeting.student = request.user
            meeting.save()
    return redirect('student_dashboard')

@login_required
@user_passes_test(is_student)
def send_chat_message(request):
    if request.method == 'POST':
        form = ChatForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
    return redirect('student_dashboard')

@login_required
def dashboard(request):
    # Get all projects created by the current user
    projects = Project.objects.filter(created_by=request.user)
   
    # Get filter parameters
    project_type = request.GET.get('type', 'all')
    status = request.GET.get('status', 'all')
    search = request.GET.get('search', '')
   
    # Apply filters
    if project_type != 'all':
        projects = projects.filter(project_type=project_type)
    if status != 'all':
        projects = projects.filter(status=status)
    if search:
        projects = projects.filter(name__icontains=search)
   
    context = {
        'projects': projects,
        'current_type': project_type,
        'current_status': status,
        'search_query': search,
    }
    return render(request, 'projects/dashboard.html', context)

@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id, created_by=request.user)
   
    if request.method == 'POST':
        # Handle assignment form
        assignment_form = AssignmentForm(request.POST)
        if assignment_form.is_valid():
            assignment = assignment_form.save(commit=False)
            assignment.project = project
            assignment.save()
            messages.success(request, f'Successfully assigned {assignment.team_member} to the project!')
            return redirect('project_detail', project_id=project.id)
    else:
        assignment_form = AssignmentForm()
   
    # Get assignments for this project
    assignments = project.assignments.all()
   
    context = {
        'project': project,
        'assignments': assignments,
        'assignment_form': assignment_form,
    }
    return render(request, 'projects/project_detail.html', context)

@login_required
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
   
    return render(request, 'projects/create_project.html', {'form': form})

@login_required
def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id, created_by=request.user)
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Project deleted successfully!')
        return redirect('dashboard')
    return render(request, 'projects/confirm_delete.html', {'project': project})

@login_required
def remove_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id, project__created_by=request.user)
    if request.method == 'POST':
        assignment.delete()
        messages.success(request, f'{assignment.team_member} removed from the project!')
        return redirect('project_detail', project_id=assignment.project.id)
    return render(request, 'projects/confirm_remove.html', {'assignment': assignment})

@login_required
def team_dashboard(request):
    # Get all assignments for the current user
    assignments = Assignment.objects.filter(team_member__user=request.user)
    context = {
        'assignments': assignments
    }
    return render(request, 'projects/team_dashboard.html', context)



@login_required
def staff_elearning(request):
    resources = LearningContent.objects.all().order_by('-created_at')
    resource_types = LearningContent.objects.values_list('type', flat=True).distinct()

    selected_type = request.GET.get('type', 'All')
    search_query = request.GET.get('search', '').strip()

    if selected_type.lower() != "all":
        resources = resources.filter(type__icontains=selected_type)

    if search_query:
        resources = resources.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    return render(request, 'projects/elearning.html', {
        'resources': resources,
        'resource_types': resource_types,
        'selected_type': selected_type,
        'search_query': search_query,
    })


@login_required
def staff_templates(request):
    templates = Template.objects.all()
    search_query = request.GET.get('search', '').strip()

    if search_query:
        templates = templates.filter(title__icontains=search_query)

    template_categories = {}
    for t in templates:
        category = t.category or "Uncategorized"
        if category not in template_categories:
            template_categories[category] = []
        template_categories[category].append(t)

    return render(request, 'projects/templates.html', {
        'template_categories': template_categories,
        'search_query': search_query,
    })
