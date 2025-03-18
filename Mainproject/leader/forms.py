from django import forms
from .models import Team,SubTaskAssigned,SubTaskSubmit

class CreateTeamFOrm(forms.ModelForm):
    class Meta:
        model=Team
        fields=['Name','Description']

class SubTaskAssForm(forms.ModelForm):
    class Meta:
        model=SubTaskAssigned
        fields=['title','Attachments','deadline',]


class SubTask_SUbmitForm(forms.ModelForm):
    class Meta:
        model = SubTaskSubmit
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