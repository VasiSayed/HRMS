from django.contrib import admin
from .models import Attendance,AttendanceDetails,Leave
# Register your models here.

admin.site.register([Attendance,AttendanceDetails,Leave])