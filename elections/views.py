from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone # Crucial for timezone-aware comparisons
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Election, Candidate, Vote, Position
from .forms import ElectionForm, PositionForm, CandidateForm, VoteForm
from .utils import encrypt_vote
# elections/templatetags/math_filters.py
from django import template
import hashlib


@login_required
def election_list(request):
    elections = Election.objects.all()
    return render(request, 'elections/election_list.html', {
        'elections': elections
    })



@login_required
def vote_view(request, election_id):
    election = get_object_or_404(Election, id=election_id)
    
    # 1. Immediate check: Is the election currently active and within time?
    # This prevents users from even seeing the form if the time has passed.
    if timezone.now() > election.end_time:
        messages.error(request, "This election has ended. You can no longer cast a vote.")
        return redirect('election_list')

    voter_hash = hashlib.sha256(str(request.user.id).encode()).hexdigest()

    # Check if the user already voted
    if Vote.objects.filter(election=election, voter_hash=voter_hash).exists():
        messages.warning(request, "You have already voted in this election.")
        return redirect('election_list')

    if request.method == 'POST':
        form = VoteForm(election, request.POST)
        if form.is_valid():
            # 2. Final check: Ensure the time didn't run out while they were filling the form
            if timezone.now() > election.end_time:
                messages.error(request, "Submission failed: The polls closed before you submitted your vote.")
                return redirect('election_list')

            candidate = form.cleaned_data['candidate']

            vote = Vote()
            vote.voter_hash = voter_hash
            vote.election = election
            vote.candidate_encrypted = encrypt_vote(str(candidate.id))
            vote.save()

            messages.success(request, "Your vote has been recorded.")
            return redirect('election_list')
    else:
        form = VoteForm(election)

    return render(request, 'elections/vote.html', {
        'form': form,
        'election': election,
        'now': timezone.now() # Useful for initial client-side sync
    })
def encrypt_vote(candidate_id):
    # candidate_id must be string
    return hashlib.sha256(str(candidate_id).encode()).hexdigest()


@login_required
def results_view(request, election_id):
    election = get_object_or_404(Election, id=election_id)
    positions = Position.objects.filter(election=election)

    total_votes = 0
    results_by_position = []

    for position in positions:
        candidates = Candidate.objects.filter(position=position)
        position_results = []

        for candidate in candidates:
            encrypted_candidate = encrypt_vote(str(candidate.id))
            count = Vote.objects.filter(
                election=election,
                candidate_encrypted=encrypted_candidate
            ).count()
            total_votes += count
            position_results.append({
                'candidate': candidate,
                'count': count
            })

        # Calculate percentages for each candidate
        for r in position_results:
            if total_votes > 0:
                r['percentage'] = (r['count'] / total_votes) * 100
            else:
                r['percentage'] = 0

        results_by_position.append({
            'position': position,
            'candidates': position_results
        })

    return render(request, 'elections/results.html', {
        'election': election,
        'results_by_position': results_by_position,
        'total_votes': total_votes
    })




def admin_required(view_func):
    """Decorator to allow only admin users"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 'admin':
            messages.error(request, "Access denied: Admins only.")
            return redirect('election_list')
        return view_func(request, *args, **kwargs)
    return wrapper

@login_required
@admin_required
def admin_dashboard(request):
    elections = Election.objects.all()
    return render(request, 'adminpanel/dashboard.html', {'elections': elections})

@login_required
@admin_required
def election_create(request):
    if request.method == 'POST':
        form = ElectionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Election created successfully.")
            return redirect('admin_dashboard')
    else:
        form = ElectionForm()
    return render(request, 'adminpanel/election_form.html', {'form': form})

@login_required
@admin_required
def position_create(request, election_id):
    election = get_object_or_404(Election, id=election_id)
    if request.method == 'POST':
        form = PositionForm(request.POST)
        if form.is_valid():
            position = form.save(commit=False)
            position.election = election
            position.save()
            messages.success(request, "Position created successfully.")
            return redirect('admin_dashboard')
    else:
        form = PositionForm()
    return render(request, 'adminpanel/position_form.html', {'form': form, 'election': election})

@login_required
@admin_required
def candidate_create(request, position_id):
    position = get_object_or_404(Position, id=position_id)
    if request.method == 'POST':
        form = CandidateForm(request.POST, request.FILES)
        if form.is_valid():
            candidate = form.save(commit=False)
            candidate.position = position
            candidate.save()
            messages.success(request, "Candidate created successfully.")
            return redirect('admin_dashboard')
    else:
        form = CandidateForm()
    return render(request, 'adminpanel/candidate_form.html', {'form': form, 'position': position})


@login_required
def candidate_create_selector(request, election_id):
    """
    Page where admin selects which position to add a candidate to.
    """
    election = get_object_or_404(Election, id=election_id)
    positions = election.positions.all()
    return render(request, 'adminpanel/candidate_selector.html', {
        'election': election,
        'positions': positions
    })

@login_required
def candidate_create(request, position_id):
    """
    Page to create a candidate for a specific position.
    """
    position = get_object_or_404(Position, id=position_id)

    if request.method == 'POST':
        form = CandidateForm(request.POST, request.FILES)
        if form.is_valid():
            candidate = form.save(commit=False)
            candidate.position = position
            candidate.save()
            messages.success(request, f"Candidate {candidate.name} added to {position.title}.")
            return redirect('admin_dashboard')
    else:
        form = CandidateForm()

    return render(request, 'adminpanel/candidate_form.html', {
        'form': form,
        'position': position
    })


register = template.Library()

@register.filter
def divide(value, arg):
    try:
        return float(value) / float(arg)
    except (ValueError, ZeroDivisionError):
        return 0


@login_required
def election_create(request):
    if request.method == "POST":
        form = ElectionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    return redirect('admin_dashboard')

# elections/views.py

def election_update(request, pk):  # <--- Change this to 'pk'
    election = get_object_or_404(Election, pk=pk)
    if request.method == "POST":
        # Don't forget request.FILES if you add images to the election later
        form = ElectionForm(request.POST, instance=election)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = ElectionForm(instance=election)
    
    # Make sure you have this template created!
    return render(request, 'elections/election_form.html', {
        'form': form, 
        'election': election
    })

@login_required
def election_delete(request, pk):
    election = get_object_or_404(Election, id=pk)
    if request.method == "POST":
        election.delete()
    return redirect('admin_dashboard')

@login_required
def position_manage(request, election_id):
    # 1. Get the specific election or show 404
    election = get_object_or_404(Election, id=election_id)
    
    # 2. Get all positions linked to this election
    # We use .prefetch_related('candidates') to load profile pics efficiently
    positions = Position.objects.filter(election=election).prefetch_related('candidates')
    
    return render(request, 'adminpanel/positions.html', {
        'election': election,
        'positions': positions,
    })

@login_required
def position_edit(request, pk):
    # Get the position we want to edit
    position = get_object_or_404(Position, pk=pk)
    election = position.election # Keep track of the parent election
    
    if request.method == "POST":
        form = PositionForm(request.POST, instance=position)
        if form.is_valid():
            form.save()
            # Redirect back to the positions list for that specific election
            return redirect('position_manage', election_id=election.id)
    else:
        form = PositionForm(instance=position)
        
    return render(request, 'adminpanel/edit_position_form.html', {
        'form': form,
        'position': position,
        'election': election
    })

@login_required
def position_delete(request, pk):
    # Handles the deletion from the positions.html page
    position = get_object_or_404(Position, pk=pk)
    election_id = position.election.id
    if request.method == 'POST':
        position.delete()
    return redirect('position_manage', election_id=election_id)


@login_required
def candidate_manage(request, election_id):
    # 1. Get the specific election or show 404
    election = get_object_or_404(Election, id=election_id)
    
    candidates = Candidate.objects.filter(
        position__election=election
    ).select_related('position')
    
    return render(request, 'adminpanel/candidates.html', {
        'election': election,
        'candidates': candidates,
    })

@login_required
def candidate_delete(request, pk):
    candidate = get_object_or_404(Candidate, id=pk)
    candidate.delete()
    return redirect('admin_dashboard')

# elections/views.py

@login_required
def candidate_edit(request, pk):
    candidate = get_object_or_404(Candidate, pk=pk)
    election = candidate.position.election

    if request.method == 'POST':
        form = CandidateForm(request.POST, request.FILES, instance=candidate)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                f"Candidate {candidate.name} updated successfully."
            )
            return redirect('candidate_manage', election_id=election.id)
    else:
        form = CandidateForm(instance=candidate)

    return render(request, 'adminpanel/edit_candidate_form.html', {
        'form': form,
        'candidate': candidate,
        'election': election,
    })
