from users.models import User,Role
from django import forms
from django.contrib.auth.forms import UserCreationForm

class Registerform(UserCreationForm):
    class Meta:
        model=User
        exclude = ['is_superuser', 'is_staff', 'user_permissions', 'groups', 'is_active', 'date_joined', 'last_login']
        fields = ['username','first_name', 'last_name',"role",'email','contact_details',"dob",'department',"manager","Team_leader"]
    def __init__(self, *args, **kwargs):
        usertype = kwargs.pop('role', None)
        super().__init__(*args, **kwargs)
        if User.objects.filter(role__RoleName="Manager").exists():
            self.fields['manager'].queryset=User.objects.filter(role__RoleName="Manager")
        else:
            self.fields['manager'].queryset=User.objects.none()
        if User.objects.filter(role__RoleName="Team Leader").exists():
            self.fields['Team_leader'].queryset=User.objects.filter(role__RoleName="Team_leader")
        else:
            self.fields['Team_leader'].queryset=User.objects.none()
        if usertype:
            self.fields['role'].queryset = Role.objects.exclude(RoleName__in=["admin", "Manager"])



class loginform(forms.Form):
    username=forms.CharField(max_length=20)
    password=forms.CharField(max_length=20,widget=forms.PasswordInput(
        attrs={
            'placeholder':'Enter Password',
        }
    ))