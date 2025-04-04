from django.contrib import admin
from users.models import  Role,User

admin.site.register([Role,User])