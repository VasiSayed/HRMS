from django.db import models
from users.models import User
from department.models import Department
from django.utils import timezone
from datetime import time


class AttendanceDetails(models.Model):
    SHIFT_CHOICES = [
        (time(6, 0), "06:00 AM"),
        (time(8, 0),  "08:00 AM"),
        (time(9, 0),  '09:00 AM'),
        (time(10, 0), "10:00 AM"),
        (time(14, 0), "02:00 PM"),
        (time(18, 0), "06:00 PM"),
        (time(19, 0), '07:00 PM'),
        (time(22, 0), "10:00 PM"),
    ]

    emp = models.OneToOneField(User, on_delete=models.PROTECT, null=False, blank=False)
    dept = models.ForeignKey(Department, on_delete=models.PROTECT, related_name="attendance_records",null=True)
    shiftStartTime = models.TimeField(choices=SHIFT_CHOICES, null=False, blank=False)
    shiftEndTime = models.TimeField(choices=SHIFT_CHOICES, null=False, blank=False)

    def __str__(self):
        return f"{self.emp.username} - {self.shiftStartTime} to {self.shiftEndTime}"


class Attendance(models.Model):
    attendance_detail = models.ForeignKey(AttendanceDetails, on_delete=models.PROTECT, null=False, blank=False)
    emp = models.ForeignKey(User, on_delete=models.PROTECT, related_name="attendance_logs", null=False, blank=False)
    date = models.DateField(auto_now_add=True)  
    startTime = models.TimeField(default=timezone.now, null=True, blank=True)
    endTime = models.TimeField(null=True, blank=True)
    Remark=models.CharField(max_length=20,choices=[('Late', 'Late'),('Over Time', 'Over Time'),('On Time', 'On Time'),],default='On Time')
    status = models.CharField(max_length=20,choices=[('Present', 'Present'),('Absent', 'Absent'),('Half day', 'Half day'),],default='Half day')

    class Meta:
        unique_together = ('emp', 'date') 
        
    def __str__(self):
        return f"{self.emp.username} - {self.date} - {self.status}"



class Leave(models.Model):
    emp = models.ForeignKey(User, on_delete=models.PROTECT, related_name="leave_requests", null=False, blank=False)
    date_from = models.DateField(null=False, blank=False)
    date_to = models.DateField(null=False, blank=False)
    document=models.FileField(upload_to="Leave_Documents/",blank=True,null=True)
    reason = models.TextField()
    Leave_type = models.CharField(max_length=2,choices=[('SL', 'Sick Leave'),('CL', 'Casual Leave'),('ML', 'Medical Leave'),('UL', 'Unpaid Leave'),],default='CL',null=False,blank=False)
    status = models.CharField(max_length=20,choices=[('Pending','Pending'),('Approved','Approved'),('Rejected','Rejected')],default='Pending')
    applied_on=models.DateField(auto_now_add=True)
    def __str__(self):
        return f"{self.emp.username} - {self.date_from} to {self.date_to} - {self.status}"