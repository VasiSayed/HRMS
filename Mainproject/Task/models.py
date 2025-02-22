from django.db import models
from users.models import User
# Create your models here.
class Task_Assigned(models.Model):
    Task=models.TextField(max_length=1000)
    Attachments=models.FileField(upload_to="Task_Assign/",blank=True,null=True)
    deadline=models.DateField(null=False,blank=False)
    Assigened_by=models.ForeignKey(User,on_delete=models.DO_NOTHING,null=False,blank=False,related_name="Task_assignment_by")
    given_on=models.DateField(auto_now_add=True)
    emp=models.ForeignKey(User,on_delete=models.DO_NOTHING,null=False,blank=False,related_name="Task_assignment_to")
    status=models.CharField(max_length=20,choices=[("complete","complete"),('submited','submited'),("pending","pending"),("In Progress","In Progress"),("Not completed","Not completed")],default="pending")

    def __str__(self):
        return f"{self.emp} Assigned by : {self.Assigened_by}"
    
    
class Task_Submitted(models.Model):
    Task=models.OneToOneField(Task_Assigned,on_delete=models.CASCADE,unique=True)
    emp=models.ForeignKey(User,on_delete=models.DO_NOTHING,null=False,blank=False,related_name="Task_Submmited_by")
    Attachments=models.FileField(upload_to="Submitted_Task/")
    submitted_on=models.DateTimeField(auto_now_add=True)
    comments=models.CharField(max_length=100,null=True,blank=True)
    status=models.CharField(max_length=20,choices=[("Approved","Approved"),("Rejected","Rejected"),("pending","pending")],default="pending")
