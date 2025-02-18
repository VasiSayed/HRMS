from .models import Department
from django import forms

class CreateDepartmntFor(forms.ModelForm):
    class Meta:
        model=Department
        exclude=("status",)

class Update_departmentView(forms.Form):
    Department_Name=forms.CharField(max_length=100)
    Description=forms.CharField(max_length=300)