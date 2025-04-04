from users.models import User,Role
from django import forms
from django.contrib.auth.forms import UserCreationForm
from datetime import time




class Registerform(UserCreationForm):
    SHIFT_CHOICES = [
        (time(6, 0), "06:00 AM"),
        (time(8, 0),  "08:00 AM"),
        (time(9, 0),  '09:00 AM'),
        (time(10, 0), "10:00 AM"),
        (time(14, 0), "02:00 PM"),
        (time(18, 0), "06:00 PM"),
        (time(19, 0), '07:00 PM'),
        (time(22, 0), "10:00 PM"),
    ]

    shiftStartTime = forms.ChoiceField(choices=SHIFT_CHOICES, label="Shift Start Time")
    shiftEndTime = forms.ChoiceField(choices=SHIFT_CHOICES, label="Shift End Time")
    class Meta:
        model=User
        exclude = ['is_superuser', 'is_staff', 'user_permissions', 'groups', 'is_active', 'date_joined', 'last_login']
        fields = ['username','first_name', 'last_name','email','contact_details',"dob"]


class RegisterManagerform(UserCreationForm):
    SHIFT_CHOICES = [
        (time(6, 0), "06:00 AM"),
        (time(8, 0),  "08:00 AM"),
        (time(9, 0),  '09:00 AM'),
        (time(10, 0), "10:00 AM"),
        (time(14, 0), "02:00 PM"),
        (time(18, 0), "06:00 PM"),
        (time(19, 0), '07:00 PM'),
        (time(22, 0), "10:00 PM"),
    ]


    shiftStartTime = forms.ChoiceField(choices=SHIFT_CHOICES, label="Shift Start Time")
    shiftEndTime = forms.ChoiceField(choices=SHIFT_CHOICES, label="Shift End Time")
    class Meta:
        model=User
        exclude = ['is_superuser', 'is_staff', 'user_permissions', 'groups', 'is_active', 'date_joined', 'last_login']
        fields = ['username','first_name', 'last_name','email','contact_details',"dob",'department']



class loginform(forms.Form):
    username=forms.CharField(max_length=20)
    password=forms.CharField(max_length=20,widget=forms.PasswordInput(
        attrs={
            'placeholder':'Enter Password',
        }
    ))