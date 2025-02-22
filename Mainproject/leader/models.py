from django.db import models
from department.models import Department
from users.models import User

# Create your models here.
class Team(models.Model):
    Name=models.CharField(max_length=100,unique=True,null=False,blank=False)
    Description=models.CharField(max_length=200,default=" ",null=False,blank=False)
    dept=models.ForeignKey(Department,on_delete=models.DO_NOTHING)
    leader=models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name="Team_leader")
    Created_by=models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name="Team_Created_By",null=True)
    Created_on=models.DateField(auto_now_add=True)
    active=models.BooleanField(default=True)



class Team_Member(models.Model):
    Team=models.ForeignKey(Team,on_delete=models.DO_NOTHING)
    Emp=models.OneToOneField(User,on_delete=models.DO_NOTHING)
    active=models.BooleanField(default=True)
    joined_on=models.DateTimeField(auto_now_add=True)



