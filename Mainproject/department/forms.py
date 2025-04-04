from .models import Department
from django import forms

WEEKDAYS = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),    
        (4, 'Friday'),
        (5, 'Saturday'),
    ]

class CreateDepartmntFor(forms.ModelForm):
    class Meta:
        model=Department
        exclude=("status",)

class Update_departmentView(forms.Form):
    Department_Name=forms.CharField(max_length=100,required=True)
    Description=forms.CharField(max_length=300)
    week_of=forms.ChoiceField(choices=WEEKDAYS)