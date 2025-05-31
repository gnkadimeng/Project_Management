from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import CostCentre, Expenditure, SupervisorProfile, SupervisorFeedback
from django.http import JsonResponse
from .models import Project
from projects.models import Submission, StudentProfile, Meeting, ChatMessage
from django.contrib.auth import get_user_model
from .forms import SupervisorFeedbackForm


@login_required
def admin_dashboard(request):
    return render(request, 'adminpanel/admin_dashboard.html')

@login_required
def admin_books(request):
    return render(request, 'adminpanel/admin_books.html')

@login_required
def app_kanban(request):
    phases = ["UX/UI", "Architecture", "Frontend", "Backend", "Testing", "Deployment"]
    return render(request, 'adminpanel/app_kanban.html', {'phases': phases})

@login_required
def admin_journals(request):
    return render(request, 'adminpanel/admin_journals.html')

@login_required
def admin_ganttchart(request):
    return render(request, 'adminpanel/admin_ganttchart.html')

@login_required
def overview(request):
    User = get_user_model()
    projects = Project.objects.all()
    users = User.objects.all()
    return render(request, 'adminpanel/overview.html', {
        'projects': projects,
        'users': users
    })

@login_required
def finance(request):
    cost_centres = CostCentre.objects.all()
    return render(request, 'adminpanel/finance.html', {'cost_centres': cost_centres})

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
        return redirect('finance')

    
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

