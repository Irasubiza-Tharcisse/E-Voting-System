from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib import messages


@login_required
def login_redirect(request):
    # Use the 'role' field to determine where they go
    if hasattr(request.user, 'role') and request.user.role == 'admin':
        return redirect('admin_dashboard')
    
    # Regular users (voters) go here
    return redirect('election_list')

def home_view(request):
    return render(request, 'users/home.html')

def register_view(request):
    if request.user.is_authenticated:
        # Send them to your traffic controller to find their correct dashboard
        return redirect('login_redirect')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('election_list')
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    # 1. STOP: If they are already logged in, send them to the redirect logic
    if request.user.is_authenticated:
        return redirect('login_redirect')

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # 2. SUCCESS: Send them to the redirect logic to check if they are Admin or User
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')
