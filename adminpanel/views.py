from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import CostCentre, Expenditure, SupervisorProfile, SupervisorFeedback
from django.http import JsonResponse
from projects.models import Project, Submission, StudentProfile, Meeting, ChatMessage, Task, Assignment
from django.contrib.auth import get_user_model
from .forms import SupervisorFeedbackForm
from django.http import JsonResponse, HttpResponseBadRequest
from decimal import Decimal, InvalidOperation
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.utils.dateparse import parse_date
from manager.models import Paper


@login_required
def admin_dashboard(request):
    return render(request, 'adminpanel/admin_dashboard.html')

@login_required
def app_kanban(request):
    phases = ["UX/UI", "Architecture", "Frontend", "Backend", "Testing", "Deployment"]
    return render(request, 'adminpanel/app_kanban.html', {'phases': phases})


@login_required
def admin_ganttchart(request):
    return render(request, 'adminpanel/admin_ganttchart.html')

@login_required
def overview(request):
    User = get_user_model()
    users = User.objects.all()

    projects = Project.objects.prefetch_related('tasks', 'assignments__team_member__user').select_related('created_by')

    for project in projects:
        tasks = project.tasks.all()
        total = tasks.count()
        completed = tasks.filter(status='done').count()
        project.progress = int((completed / total) * 100) if total else 0

        # Use first assigned team member if available
        if project.assignments.exists():
            assignment = project.assignments.first()
            project.assigned_user = assignment.team_member.user
        else:
            project.assigned_user = project.created_by

    return render(request, 'adminpanel/overview.html', {
        'projects': projects,
        'users': users
    })


@login_required
def finance(request):
    cost_centres = CostCentre.objects.all()
    all_expenditures = Expenditure.objects.select_related('cost_centre').all()

    # Total spent per category
    category_totals = (
        Expenditure.objects.values('category')
        .annotate(total=Sum('amount'))
        .order_by('category')
    )

    monthly_totals = (
        Expenditure.objects
        .values('month')
        .annotate(total=Sum('amount'))
        .order_by('month')
    )

    return render(request, 'adminpanel/finance.html', {
        'cost_centres': cost_centres,
        'all_expenditures': all_expenditures,
        'category_totals': category_totals,
        'monthly_totals': monthly_totals,
    })

@login_required
def add_cost_centre(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        received = request.POST.get('received')
        if name and received:
            CostCentre.objects.create(
                name=name,
                total_received=received,
                total_spent=0
            )
            return JsonResponse({'message': 'Cost Centre added successfully'})
        return HttpResponseBadRequest('Missing fields')
    return HttpResponseBadRequest('Invalid request')
    
@login_required
def add_expenditure(request):
    if request.method == 'POST':
        cost_centre_id = request.POST.get('cost_centre_id')
        month = request.POST.get('month')
        name = request.POST.get('name')
        category = request.POST.get('category')

        # Safely convert numeric fields
        try:
            amount = Decimal(request.POST.get('amount', '0') or '0.00')
            oracle = Decimal(request.POST.get('oracle_balance', '0') or '0.00')
        except InvalidOperation:
            return HttpResponseBadRequest("Invalid number format")

        cost_centre = CostCentre.objects.get(id=cost_centre_id)
        Expenditure.objects.create(
            cost_centre=cost_centre,
            month=month,
            name=name,
            category=category,
            amount=amount,
            oracle_balance=oracle
        )
        return redirect('finance')


@login_required
def get_expenditures(request, cost_centre_id):
    cost_centre = CostCentre.objects.get(id=cost_centre_id)
    expenditures = cost_centre.expenditures.all()
    data = []
    for exp in expenditures:
        data.append({
            'month': exp.month,
            'name': exp.name,
            'category': exp.category,
            'amount': str(exp.amount),
            'opening_balance': str(exp.opening_balance),
            'closing_balance': str(exp.closing_balance),
            'oracle_balance': str(exp.oracle_balance),
        })
    return JsonResponse({'expenditures': data})

@login_required
def delete_cost_centre(request, pk):
    cost_centre = get_object_or_404(CostCentre, pk=pk)
    if request.method == 'POST':
        cost_centre.delete()
        return redirect('finance')
    return render(request, 'adminpanel/confirm_delete.html', {'cost_centre': cost_centre})

@login_required
def edit_cost_centre(request, pk):
    cost_centre = get_object_or_404(CostCentre, pk=pk)
    if request.method == 'POST':
        cost_centre.name = request.POST.get('name')
        cost_centre.total_received = request.POST.get('total_received')
        cost_centre.save()
        return redirect('finance')
    return redirect('finance')  # fallback if GET request

@login_required
def edit_expenditure(request, pk):
    expenditure = get_object_or_404(Expenditure, pk=pk)
    if request.method == 'POST':
        expenditure.month = request.POST.get('month')
        expenditure.name = request.POST.get('name')
        expenditure.category = request.POST.get('category')
        expenditure.amount = Decimal(request.POST.get('amount', '0'))
        expenditure.oracle_balance = Decimal(request.POST.get('oracle_balance', '0'))
        expenditure.save()
        return redirect('finance')
    return redirect('finance')

@login_required
def delete_expenditure(request, pk):
    expenditure = get_object_or_404(Expenditure, pk=pk)
    if request.method == 'POST':
        expenditure.delete()
        return redirect('finance')
    return redirect('finance')


@login_required
def admin_kanban(request):
    return render(request, 'adminpanel/admin_kanban.html')

# @login_required
# def supervisor_dashboard(request):
#     return render(request, 'adminpanel/supervisor_dashboard.html')

def is_supervisor(user):
    return user.is_authenticated and user.role == 'admin'


@login_required
@user_passes_test(is_supervisor)
def provide_feedback(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)
    supervisor = request.user.supervisorprofile
    if request.method == 'POST':
        form = SupervisorFeedbackForm(request.POST, request.FILES)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.submission = submission
            feedback.supervisor = supervisor
            feedback.save()

            # Optionally update submission status directly
            submission.status = feedback.status
            submission.feedback_text = feedback.comments
            if feedback.uploaded_file:
                submission.feedback_file = feedback.uploaded_file
            submission.save()

            return redirect('supervisor_dashboard')  # or your submissions page
    else:
        form = SupervisorFeedbackForm()

    return render(request, 'adminpanel/provide_feedback.html', {
        'form': form,
        'submission': submission
    })

# @login_required
# @user_passes_test(is_supervisor)
# def supervisor_dashboard(request):
#     supervisor = request.user.supervisorprofile
#     submissions = Submission.objects.filter(student__supervisor=request.user)
#     meetings = Meeting.objects.filter(supervisor=supervisor)
#     chat_messages = ChatMessage.objects.filter(sender=request.user)  # adjust filter if needed
#     chat_form = ChatForm()
#     meeting_form = MeetingRequestForm()

#     return render(request, 'adminpanel/supervisor_dashboard.html', {
#         'submissions': submissions,
#         'meetings': meetings,
#         'chat_messages': chat_messages,
#         'chat_form': chat_form,
#         'meeting_form': meeting_form,
#     })

@login_required
@user_passes_test(lambda u: u.role == 'admin')
def supervisor_dashboard(request):
    supervisor = request.user  # This is the CustomUser with role='admin'

    # Step 1: Find students supervised by this admin
    supervised_student_users = StudentProfile.objects.filter(supervisor=supervisor).values_list('user', flat=True)

    # Step 2: Filter submissions for those student users
    submissions = Submission.objects.filter(student__in=supervised_student_users)

    meetings = Meeting.objects.filter(student__in=supervised_student_users)
    chat_messages = ChatMessage.objects.filter(sender=request.user)
    # chat_form = ChatForm()
    # meeting_form = MeetingRequestForm()

    return render(request, 'adminpanel/supervisor_dashboard.html', {
        'submissions': submissions,
        'meetings': meetings,
        'chat_messages': chat_messages,
        # 'chat_form': chat_form,
        # 'meeting_form': meeting_form,
    })

@login_required
def admin_journal(request):
    internal_papers = Paper.objects.filter(internal_external='internal').order_by('-updated_at')
    external_papers = Paper.objects.filter(internal_external='external').order_by('-updated_at')
    
    return render(request, 'adminpanel/admin_journal.html', {
        'internal_papers': internal_papers,
        'external_papers': external_papers,
    })

@login_required
def admin_book(request):
    return render(request, 'adminpanel/admin_book.html')

def admin_required(view_func):
    return user_passes_test(lambda u: u.is_authenticated and u.role == 'admin')(view_func)

@admin_required
def admin_user_kanban(request, user_id):
    user = get_object_or_404(get_user_model(), id=user_id)
    tasks = Task.objects.filter(assigned_to=user)

    # Group by status
    task_data = {
        'todo': tasks.filter(status='todo'),
        'in_progress': tasks.filter(status='in_progress'),
        'review': tasks.filter(status='review'),
        'done': tasks.filter(status='done'),
    }

    return render(request, 'adminpanel/partials/user_kanban.html', {
        'user': user,
        'task_data': task_data
    })
