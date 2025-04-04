from django.db import models
from department.models import Department
from users.models import User
from django.utils import timezone
# Create your models here. 

Rating_choices = [
        (3, 'Bad'),
        (5, 'Average'),
        (8, 'Good'),
        (10, 'Very Good'),
    ]


class Team(models.Model):
    Name=models.CharField(max_length=100,unique=True,null=False,blank=False)
    Description=models.CharField(max_length=200,default=" ",null=False,blank=False)
    dept=models.ForeignKey(Department,on_delete=models.DO_NOTHING)
    leader=models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name="Team_leader")
    Created_by=models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name="Team_Created_By",null=True)
    Created_on=models.DateField(default=timezone.now)
    active=models.BooleanField(default=True)
    def __str__(self):
        return f"Team Name :- {self.Name} Leader :- {self.leader.username}"


class Team_Member(models.Model):
    Team=models.ForeignKey(Team,on_delete=models.DO_NOTHING)
    Emp=models.ForeignKey(User,on_delete=models.DO_NOTHING)
    joined_on=models.DateTimeField(default=timezone.now)
    active=models.BooleanField(default=True)

    def __str__(self):
        return f"{Team.Name} Member :- {self.Emp.username}"


class SubTaskAssigned(models.Model):
    title=models.TextField(max_length=300)
    Attachments=models.FileField(upload_to="TeamSubTask_Assign/",blank=True,null=True)
    deadline=models.DateField(null=False,blank=False)
    Team=models.ForeignKey(Team,related_name="which_teams_task",on_delete=models.PROTECT)
    emp=models.ForeignKey(User,on_delete=models.PROTECT)
    Assigned_on=models.DateField(default=timezone.now)
    status=models.CharField(max_length=20,
                            choices=[
                                ("complete","complete"),
                                ('submited','submited'),
                                ("pending","pending"),
                                ("In Progress","In Progress"),
                                ("Not completed","Not completed")
                                ],
                                default="pending")
    def __str__(self):
        return f"Sub Task of {self.Team} emp :{self.emp}"

class SubTaskSubmit(models.Model):
    subtask=models.OneToOneField('leader.SubTaskAssigned',on_delete=models.PROTECT,related_name="TeamSubTasksubmitted")
    emp=models.ForeignKey(User,on_delete=models.PROTECT,null=False,blank=False,related_name="TaskSubSubmmited_by")
    Attachments=models.FileField(upload_to="TeamSubSubmitted_Task/",blank=True,null=True)
    submitted_on=models.DateTimeField(default=timezone.now)
    comments=models.CharField(max_length=100,null=True,blank=True)
    status=models.CharField(max_length=20,choices=[("Approved","Approved"),("Rejected","Rejected"),("pending","pending")],default="pending")
    score = models.IntegerField(null=True,blank=False,choices=Rating_choices)

    
    def __str__(self):
        return f" Team Task Submited Team:-{self.subtask.Team.Name} submited by: {self.emp} "