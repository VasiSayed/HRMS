from django.db import models
from users.models import User
from django.utils import timezone
# Create your models here.
    

class Task_Assigned(models.Model):
    Task=models.TextField(max_length=300)
    Attachments=models.FileField(upload_to="Task_Assign/",blank=True,null=True)
    deadline=models.DateField(null=False,blank=False)
    Assigened_by=models.ForeignKey(User,on_delete=models.PROTECT,null=False,blank=False,related_name="Task_assignment_by")
    given_on=models.DateField(default=timezone.now)
    emp=models.ForeignKey(User,on_delete=models.PROTECT,null=False,blank=False,related_name="Task_assignment_to")
    status=models.CharField(max_length=20,choices=[("complete","complete"),('submited','submited'),("pending","pending"),("In Progress","In Progress"),("Not completed","Not completed")],default="pending")

    def __str__(self):
        return f"{self.emp} Assigned by : {self.Assigened_by}"
    

Rating_choices = [
        (2.5, 'Bad'),
        (5, 'Average'),
        (7.5, 'Good'),
        (10, 'Very Good'),
    ]



class Task_Submitted(models.Model):
    Task=models.OneToOneField(Task_Assigned,on_delete=models.CASCADE,unique=True)
    emp=models.ForeignKey(User,on_delete=models.PROTECT,null=False,blank=False,related_name="Task_Submmited_by")
    Attachments=models.FileField(upload_to="Submitted_Task/",blank=True,null=True)
    submitted_on=models.DateTimeField(default=timezone.now)
    comments=models.CharField(max_length=100,null=True,blank=True)
    status=models.CharField(max_length=20,choices=[("Approved","Approved"),("Rejected","Rejected"),("pending","pending")],default="pending")
    score = models.CharField(max_length=4,null=True,blank=False,choices=Rating_choices)



class TeamTaskAssign(models.Model):
    title=models.TextField(max_length=300)
    Attachments=models.FileField(upload_to="TeamTask_Assign/",blank=True,null=True)
    deadline=models.DateField(null=False,blank=False)
    Assigened_by=models.ForeignKey(User,on_delete=models.PROTECT,null=False,blank=False,related_name="_TeamTask_assignment_by")
    given_on=models.DateField(default=timezone.now)
    Team=models.ForeignKey('leader.Team',on_delete=models.PROTECT,null=False,blank=False,related_name="Task_assignment_to_team")
    status=models.CharField(max_length=20,choices=[("complete","complete"),('submited','submited'),("pending","pending"),("In Progress","In Progress"),("Not completed","Not completed")],default="pending")


class TeamTaskSubmitted(models.Model):
    Task=models.OneToOneField(TeamTaskAssign,on_delete=models.CASCADE,unique=True)
    Attachments=models.FileField(upload_to="TeamSubmitted_Task/",blank=True,null=True)
    submitted_on=models.DateTimeField(default=timezone.now)
    submitted_by=models.ForeignKey(User,on_delete=models.PROTECT)
    comments=models.CharField(max_length=100,null=True,blank=True)
    status=models.CharField(max_length=20,choices=[("Approved","Approved"),("Rejected","Rejected"),("pending","pending")],default="pending")
    score = models.CharField(max_length=4,null=True,blank=False,choices=Rating_choices)
    