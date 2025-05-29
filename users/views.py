from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import CustomUserCreationForm, CustomLoginForm

def register_view(request):
    form = CustomUserCreationForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('login')  # new users go to normal dashboard
    return render(request, 'users/login.html', {'form': form})

def login_view(request):
    form = CustomLoginForm(data=request.POST or None)
    if form.is_valid():
        user = form.get_user()
        login(request, user)

        # Redirect based on user role
        if user.role == 'admin':
            return redirect('admin_dashboard') # Admin
        elif user.role == 'manager':
            return redirect('manager_dashboard') # Project Manager
        elif user.role == 'student':
            return redirect('student_dashboard')  # Student
        else:
            return redirect('dashboard') # Staff
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')
