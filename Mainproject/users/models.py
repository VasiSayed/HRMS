from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from department.models import Department

gender_choice = [
    ("M","Male"),
    ("F","Female"),
    ("O","Other"),
    ("N","Don't want to mention"),
]


class Role(models.Model):
    RoleName=models.CharField(max_length=50,unique=True)
    description=models.CharField(max_length=200,null=False,default=" ")
    def __str__(self):
        return f"{self.RoleName}"



class User(AbstractUser):
    role=models.ForeignKey(Role,on_delete=models.DO_NOTHING,null=True,blank=False)
    contact_details = models.CharField(max_length=13,default="",null=False,blank=False)
    gender=models.CharField(max_length=10,choices=gender_choice,default="Male")
    dob=models.DateField(null=True)
    department=models.ForeignKey(Department,on_delete=models.SET_NULL,null=True,blank=False)
    manager=models.ForeignKey('self',on_delete=models.SET_NULL,null=True,blank=True,related_name="Manager")
    created_on=models.DateField(auto_now_add=True)  
    active=models.BooleanField(default=True)  
    def Namee(self):
        return f"{self.first_name} {self.last_name} "

    def __str__(self):
        return f"{self.role} : {self.username}  - {self.department}"