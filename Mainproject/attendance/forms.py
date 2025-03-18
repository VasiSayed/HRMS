from users.models import User
from .models import Leave
from django import forms
from datetime import time


class Leaveform(forms.ModelForm):
    class Meta:
        model=Leave
        exclude=('status','emp')