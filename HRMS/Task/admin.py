from django.contrib import admin
from Task.models import Task_Assigned,Task_Submitted,TeamTaskAssign,TeamTaskSubmitted
# Register your models here.


admin.site.register([Task_Assigned,Task_Submitted,TeamTaskSubmitted,TeamTaskAssign])