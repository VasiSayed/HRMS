from users.models import User
from department.models import Department
from django.shortcuts import render,redirect
from Task.models import Task_Assigned,Task_Submitted

def Base_view(request):
    if not (request.user.is_authenticated):
        return redirect('login')
    
    if request.user.is_authenticated and (request.user.role.RoleName == "admin" or request.user.is_superuser):
        context={
            "count_Dept":Department.objects.count() if Department.objects.exists() else "No",
            "count_emp":User.objects.filter(role__RoleName="Employee").count() if User.objects.filter(role__RoleName="Employee").exists() else "No",
            "manager_count":User.objects.filter(role__RoleName="Manager",).count() if User.objects.filter(role__RoleName="Manager").exists() else "No" ,
            }
        return render(request,'base.html',context)
    if request.user.is_authenticated and request.user.role.RoleName=="Manager":
        context={
            "total_task":Task_Assigned.objects.filter(Assigened_by=request.user).count() if Task_Assigned.objects.filter(Assigened_by=request.user).exists() else "No Task Given",
            "Comp_task":Task_Submitted.objects.filter(Task__Assigened_by=request.user,status="Approved").count() if Task_Submitted.objects.filter(Task__Assigened_by=request.user,status="Approved").exists() else "0",
            "count_emp":User.objects.filter(role__RoleName="Employee",department=request.user.department).count() if User.objects.filter(role__RoleName="Employee",department=request.user.department).exists() else "No",
        }
        return render(request,'base.html',context)
    if request.user.is_authenticated and request.user.role.RoleName=="Employee":
        context={
            "total_task":Task_Assigned.objects.filter(emp=request.user).count() if Task_Assigned.objects.filter(emp=request.user).exists() else "No Task Given",
            "Comp_task":Task_Assigned.objects.filter(emp=request.user,status="complete").count() if Task_Assigned.objects.filter(emp=request.user,status="complete").exists() else "0",   
            "Pend_task":Task_Assigned.objects.filter(emp=request.user,status="pending").count() if Task_Assigned.objects.filter(emp=request.user,status="pending").exists() else "0",   
        }
        return render(request,'base.html',context) 
    return render(request,'base.html')

