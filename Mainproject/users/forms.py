from users.models import User,Role
from django import forms
from django.contrib.auth.forms import UserCreationForm

class Registerform(UserCreationForm):
    class Meta:
        model=User
        exclude = ['is_superuser', 'is_staff', 'user_permissions', 'groups', 'is_active', 'date_joined', 'last_login']
        fields = ['username','first_name', 'last_name','email','contact_details',"dob"]


class RegisterManagerform(UserCreationForm):
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