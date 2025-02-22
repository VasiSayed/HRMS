from django import forms
from Task.models import Task_Assigned,Task_Submitted
from users.models import User

class TaskFOrm(forms.ModelForm):
    class Meta:
        model = Task_Assigned
        fields=['Task','Attachments','deadline']

class SubmitForm(forms.ModelForm):
    class Meta:
        model = Task_Submitted
        fields = ['Attachments', 'comments']
        widgets = {
            'comments': forms.Textarea(attrs={
                'placeholder': 'Add your comments here...',
                'rows': 4
            }),
            'Attachments': forms.FileInput(attrs={
                'accept': '*/*'  # Accept all file types
            })
        }
        