# projects/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import DailyTask, StudentProfile, Submission, Notification, Meeting, ChatMessage
from .forms import DailyTaskForm, StudentProfileForm, SubmissionForm, FeedbackReplyForm, MeetingForm, ChatForm
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import date
from django.utils.timezone import now
from tasks.forms import FileUploadForm


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
    return render(request, 'projects/staff_kanban.html')

@login_required
def journals_view(request):
    return render(request, 'projects/journals.html')

@login_required
def books_view(request):
    return render(request, 'projects/books.html')

@login_required
def projects_review(request):
    return render(request, 'projects/projects_review.html')

@login_required
def ganttchart(request):
    return render(request, 'projects/ganttchart.html')

@login_required
def elearning(request):
    return render(request, 'projects/elearning.html')

@login_required
def templates(request):
    return render(request, 'projects/templates.html')

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

