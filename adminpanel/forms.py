from django import forms
from elections.models import Election, Position, Candidate
class ElectionForm(forms.ModelForm):
    class Meta:
        model = Election
        fields = ['title', 'description', 'start_time', 'end_time']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control bg-body text-body border-secondary-subtle'}),
            'description': forms.Textarea(attrs={'class': 'form-control bg-body text-body border-secondary-subtle', 'rows': 2}),
            'start_time': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control native-datetime bg-body text-body border-secondary-subtle',
            }),
            'end_time': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control native-datetime bg-body text-body border-secondary-subtle',
            }),
        }
        
class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ['title', 'election']

class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['position', 'name', 'photo', 'manifesto']
