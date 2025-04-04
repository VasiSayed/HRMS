from users.models import User
from department.models import Department
from django.shortcuts import render,redirect
from Task.models import Task_Assigned,Task_Submitted,TeamTaskSubmitted,TeamTaskAssign
from leader.models import Team
from django.db.models import Q
from attendance.models import Attendance,Leave
from datetime import date
from leader.models import SubTaskAssigned,Team_Member

def Base_view(request):
    if not (request.user.is_authenticated):
        return redirect('login')
    
    if request.user.is_authenticated and (request.user.role.RoleName == "admin" or request.user.is_superuser):
        context={
            "count_Dept":Department.objects.count() if Department.objects.exists() else "No",
            "count_emp":User.objects.filter( Q( role__RoleName="Employee") | Q( role__RoleName= "Team Leader" )).count() if User.objects.filter( Q( role__RoleName="Employee") | Q( role__RoleName= "Team Leader" )).exists() else "No",
            "manager_count":User.objects.filter(role__RoleName="Manager",).count() if User.objects.filter(role__RoleName="Manager").exists() else "No" ,
            'Active_team_count':Team.objects.filter(active=True).count() if Team.objects.filter(active=True).exists() else "No",            
            'team_count':Team.objects.filter().count() if Team.objects.filter().exists() else "No",  
            'lpendng':Leave.objects.filter(emp__role__RoleName='Manager',status='Pending').count() if Leave.objects.filter(emp__role__RoleName='Manager',status='Pending').exists() else "0"

            }
        return render(request,'base.html',context)
    if request.user.is_authenticated and request.user.role.RoleName=="Manager":
        context={
            "total_task":Task_Assigned.objects.filter(Assigened_by=request.user).count() if Task_Assigned.objects.filter(Assigened_by=request.user).exists() else "0",
            "Comp_task":Task_Submitted.objects.filter(Task__Assigened_by=request.user,status="Approved").count() if Task_Submitted.objects.filter(Task__Assigened_by=request.user,status="Approved").exists() else "0",
            "count_emp":User.objects.filter(Q( role__RoleName="Employee") | Q( role__RoleName= "Team Leader" ),department=request.user.department).count() if User.objects.filter(Q( role__RoleName="Employee") | Q( role__RoleName= "Team Leader" ),department=request.user.department).exists() else "No",
            'Active_team_count':Team.objects.filter(Created_by=request.user,active=True).count() if Team.objects.filter(Created_by=request.user,active=True).exists() else "No",            
            'team_count':Team.objects.filter(Created_by=request.user).count() if Team.objects.filter(Created_by=request.user).exists() else "No", 
            'lpendng':Leave.objects.filter(emp__manager=request.user,status='Pending').count() if Leave.objects.filter(emp__manager=request.user,status='Pending').exists() else "0",
        }
        print('this is the count',context['lpendng'])

        return render(request,'base.html',context)
    if request.user.is_authenticated and request.user.role.RoleName=="Team Leader":
        context={
            "total_task":Task_Assigned.objects.filter(emp=request.user).count() if Task_Assigned.objects.filter(emp=request.user).exists() else "No Task Given",
            "Comp_task":Task_Assigned.objects.filter(emp=request.user,status="complete").count() if Task_Assigned.objects.filter(emp=request.user,status="complete").exists() else "0",   
            "Pend_task":Task_Assigned.objects.filter(emp=request.user,status="pending").count() if Task_Assigned.objects.filter(emp=request.user,status="pending").exists() else "0",   
            'team_count':Team.objects.filter(leader=request.user,active=True).count() if Team.objects.filter(leader=request.user,active=True).exists() else "No",     
            'Team_pen_task' : TeamTaskAssign.objects.filter(status='pending',Team__leader=request.user,Team__active=True).count() if TeamTaskAssign.objects.filter(status='pending',Team__leader=request.user,Team__active=True).exists() else '0',
            'Team_Member_pen_task':SubTaskAssigned.objects.filter(Team__leader=request.user,Team__active=True,status='pending').count() if SubTaskAssigned.objects.filter(Team__leader=request.user,Team__active=True,status='pending').exists() else '0',
        }

        if Team.objects.filter(leader=request.user,active=True).exists():
            context.update({"Active team_count":Team.objects.filter(leader=request.user,active=True).count() }) 

            if TeamTaskSubmitted.objects.filter(Task__Assigened_by=request.user,status="pending").exists():
                PEnding_Team_ask=TeamTaskSubmitted.objects.filter(Task__Assigened_by=request.user,status="pending").count()
                context.update({"Pen_check_Sub_Task":PEnding_Team_ask})            

        return render(request,'base.html',context) 
    
    if request.user.is_authenticated and request.user.role.RoleName=="Employee":
        context={
            "total_task":Task_Assigned.objects.filter(emp=request.user).count() if Task_Assigned.objects.filter(emp=request.user).exists() else "No Task Given",
            "Comp_task":Task_Assigned.objects.filter(emp=request.user,status="complete").count() if Task_Assigned.objects.filter(emp=request.user,status="complete").exists() else "0",   
            "Pend_task":Task_Assigned.objects.filter(emp=request.user,status="pending").count() if Task_Assigned.objects.filter(emp=request.user,status="pending").exists() else "0",  
            'SubTeamTask':SubTaskAssigned.objects.filter(status='pending',emp=request.user).count() if SubTaskAssigned.objects.filter(status='pending',emp=request.user).exists() else '0', 
            'Active_team_count':Team_Member.objects.filter(Emp=request.user, Team__active=True).count() if Team_Member.objects.filter(Emp=request.user, Team__active=True).exists() else '0',
            
        }
        # try:
        #      atten=Attendance.objects.get(emp=request.user,date=date.today())
        #      if atten.endTime is None:
        #           context.update({'out':"hi"})    
                           
        # except Attendance.DoesNotExist:
        #     context.update({'Atten':"hi"})
        return render(request,'base.html',context) 
    return render(request,'base.html')


