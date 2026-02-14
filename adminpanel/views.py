from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import admin_required
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib.sessions.models import Session
from django.contrib.auth.decorators import login_required
from .forms import ElectionForm, PositionForm, CandidateForm
from elections.models import Election, Position, Candidate
from users.models import CustomUser

User = get_user_model()

@login_required
@admin_required
def dashboard(request):
    # Get all elections
    elections = Election.objects.all().order_by('-start_time')  # latest first
    form = ElectionForm() # Make sure this instance is created
    active_sessions_count = Session.objects.filter(expire_date__gte=timezone.now()).count()
    total_voters_count = User.objects.exclude(role='admin').count()
    return render(request, 'adminpanel/dashboard.html', 
                  {'elections': elections,'form': form, 
                   'active_sessions': active_sessions_count,
                   'total_votes': total_voters_count,})
@admin_required
@login_required
def manage_admins(request):
    # Use getattr to avoid AttributeErrors if the field is missing
    user_role = getattr(request.user, 'role', None)
    is_approved = getattr(request.user, 'is_approved', False)

    if user_role != 'admin' or not is_approved:
        messages.error(request, "You do not have permission to view this page.")
        return redirect('election_list')
        
    pending_admins = User.objects.filter(role='admin', is_approved=False).order_by('-date_joined')
    return render(request, 'adminpanel/manage_admins.html', {'pending_admins': pending_admins})

@login_required
def approve_admin(request, user_id):
    # Security: Only an already approved admin can approve others
    if request.user.role != 'admin' or not request.user.is_approved:
        messages.error(request, "Unauthorized access.")
        return redirect('election_list')

    if request.method == 'POST':
        target_user = get_object_or_404(User, id=user_id)
        
        # Ensure we are only approving someone who is actually an admin
        if target_user.role == 'admin':
            target_user.is_approved = True
            target_user.save()
            messages.success(request, f"Access granted! {target_user.username} is now an active administrator.")
        else:
            messages.warning(request, "The selected user is not an administrator.")
            
    return redirect('manage_admins')

@login_required
def deny_admin(request, user_id):
    # Security check
    if request.user.role != 'admin' or not request.user.is_approved:
        messages.error(request, "Unauthorized access.")
        return redirect('election_list')

    if request.method == 'POST':
        target_user = get_object_or_404(User, id=user_id)
        
        # We delete the user object if denied to prevent ghost accounts
        username = target_user.username
        target_user.delete()
        messages.info(request, f"Administrator request for {username} has been denied and removed.")
            
    return redirect('manage_admins')


def manage_elections(request):
    elections = Election.objects.all()
    form = ElectionForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('admin_elections')
    return render(request, 'adminpanel/elections.html', {'form': form, 'elections': elections})

@admin_required
def manage_positions(request):
    positions = Position.objects.all()
    form = PositionForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('admin_positions')
    return render(request, 'adminpanel/positions.html', {'form': form, 'positions': positions})

@admin_required
def manage_candidates(request):
    candidates = Candidate.objects.all()
    form = CandidateForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('admin_candidates')
    return render(request, 'adminpanel/candidates.html', {'form': form, 'candidates': candidates})
