from django import forms
from .models import Team

class CreateTeamFOrm(forms.ModelForm):
    class Meta:
        model=Team
        fields=['Name','Description']

