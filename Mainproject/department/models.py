from django.db import models
# Create your models here.

class Department(models.Model):
    dept_id= models.BigAutoField(primary_key=True,auto_created=True)
    dept_name=models.CharField(max_length=100,unique=True,null=False)
    description=models.CharField(max_length=300,null=False)
    create_at=models.DateTimeField (auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    status=models.BooleanField(default=True)

    def __str__(self):
        return f"{self.dept_name}"

