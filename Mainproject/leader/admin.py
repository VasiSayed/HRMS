from django.contrib import admin
from .models import Team,Team_Member,SubTaskAssigned,SubTaskSubmit
# Register your models here.


admin.site.register([Team,Team_Member,SubTaskSubmit,SubTaskAssigned])