from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from tasks.models import Task
from .models import Comment, FileUpload
from .forms import CommentForm, FileUploadForm
from notifications.models import Notification
import re


@login_required
def collaboration_overview(request):
    user_tasks = Task.objects.filter(assigned_to=request.user)
    all_tasks = Task.objects.all().order_by('-created_at')

    context = {
        'my_tasks': user_tasks,
        'all_tasks': all_tasks,
    }
    return render(request, 'collaborations/collaboration_dashboard.html', context)


@login_required
def view_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    comments = task.comments.all().order_by('-created_at')
    files = task.files.all().order_by('-uploaded_at')

    comment_form = CommentForm()
    file_form = FileUploadForm()

    if request.method == 'POST':
        if 'add_comment' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.task = task
                comment.user = request.user
                comment.save()

                # Handle @mentions
                mentioned_usernames = re.findall(r'@(\w+)', comment.content)
                for username in mentioned_usernames:
                    try:
                        mentioned_user = User.objects.get(username=username)
                        if mentioned_user != request.user:
                            Notification.objects.create(
                                user=mentioned_user,
                                message=f"You were mentioned in a comment on task '{task.title}'."
                            )
                    except User.DoesNotExist:
                        pass

                # Notify task owner
                if task.assigned_to != request.user:
                    Notification.objects.create(
                        user=task.assigned_to,
                        message=f"{request.user.username} commented on your task '{task.title}'."
                    )

                return redirect('view_task', task_id=task_id)

        if 'upload_file' in request.POST:
            file_form = FileUploadForm(request.POST, request.FILES)
            if file_form.is_valid():
                file_upload = file_form.save(commit=False)
                file_upload.task = task
                file_upload.save()
                messages.success(request, "File uploaded.")
                return redirect('view_task', task_id=task_id)

    return render(request, 'collaborations/task_detail.html', {
        'task': task,
        'comments': comments,
        'files': files,
        'comment_form': comment_form,
        'file_form': file_form,
        'user': request.user
    })


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    task_id = comment.task.id
    comment.delete()
    messages.success(request, "Comment deleted.")
    return redirect('view_task', task_id=task_id)


@login_required
def delete_file(request, file_id):
    file = get_object_or_404(FileUpload, id=file_id)
    if file.task.assigned_to == request.user:
        task_id = file.task.id
        file.delete()
        messages.success(request, "File deleted.")
        return redirect('view_task', task_id=task_id)
    return redirect('view_task', task_id=file.task.id)
