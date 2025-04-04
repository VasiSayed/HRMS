from django import forms
from Task.models import Task_Assigned,Task_Submitted,TeamTaskAssign,TeamTaskSubmitted

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
                'accept': '*/*' 
            })
        }
        
class TeamTaskAssignForm(forms.ModelForm):
    class Meta:
        model = TeamTaskAssign
        fields=['title','Attachments','deadline']


class TeamTaskSubmitForm(forms.ModelForm):
    class Meta:
        model = TeamTaskSubmitted
        fields = ['Attachments', 'comments']
        widgets = {
            'comments': forms.Textarea(attrs={
                'placeholder': 'Add your comments here...',
                'rows': 4
            }),
            'Attachments': forms.FileInput(attrs={
                'accept': '*/*' 
            })
        }