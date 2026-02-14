from django import forms
from .models import Election, Position, Candidate

# forms.py
from django import forms
from .models import Vote, Candidate
import hashlib

class VoteForm(forms.Form):
    candidate = forms.ModelChoiceField(
        queryset=Candidate.objects.none(),  # will be set dynamically
        widget=forms.RadioSelect,
        empty_label=None,
        label="Select a Candidate"
    )

    def __init__(self, election=None, *args, **kwargs):
        """
        Dynamically set candidates based on the election.
        """
        super().__init__(*args, **kwargs)
        if election:
            # Only include candidates belonging to positions in this election
            self.fields['candidate'].queryset = Candidate.objects.filter(
                position__election=election
            )


from django import forms
from .models import Election

class ElectionForm(forms.ModelForm):
    class Meta:
        model = Election
        fields = ['title', 'description', 'start_time', 'end_time']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control bg-body text-body border-secondary-subtle'}),
            'description': forms.Textarea(attrs={'class': 'form-control bg-body text-body border-secondary-subtle', 'rows': 2}),
            
            # Start Date & Time
            'start_time': forms.DateTimeInput(attrs={
                'type': 'datetime-local', # Combined native picker
                'class': 'form-control bg-body text-body border-secondary-subtle',
            }),
            
            # End Date & Time
            'end_time': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control bg-body text-body border-secondary-subtle',
            }),
        }

class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. President'}),
            'max_votes': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }

class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['name', 'photo', 'manifesto']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Candidate full name'
            }),
            'photo': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
            'manifesto': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Candidate manifesto'
            }),
        }

