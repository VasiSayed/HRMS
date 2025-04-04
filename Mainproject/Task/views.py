from department.models import Department
from django.shortcuts import render,get_object_or_404,redirect
from users.models import User
from django.views import View
from .forms import TaskFOrm,SubmitForm,TeamTaskAssignForm,TeamTaskSubmitForm
from .models import Task_Assigned,Task_Submitted,TeamTaskAssign,TeamTaskSubmitted
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, HttpResponse
import mimetypes
from django.db.models import Q
from leader.models import Team,SubTaskAssigned,SubTaskSubmit
from django.db.models import Case, When, Value, IntegerField
from datetime import date
# Create your views here.

@login_required
def allemp(request):
    if request.user.role.RoleName not in ["admin", "Manager"]:
        messages.error(request, 'Not authorized')
        return redirect('home')
    
    if request.user.role.RoleName=="admin":
            context={
            "emp" : User.objects.filter((Q (role__RoleName="Employee") | Q(role__RoleName="Team Leader") ))
            }
            return render(request,'Task/allEmp.html',context)
    
    elif request.user.role.RoleName=="Manager":
            context={
            "emp" : User.objects.filter((Q (role__RoleName="Employee") | Q(role__RoleName="Team Leader") ),department=request.user.department)
            }
            print(context)
            return render(request,'Task/allEmp.html',context)


class Task_assignment(View):
    def get(self,request,id):
        context={
            "form":TaskFOrm(),
            "title":"Assign Task",
             "admi":get_object_or_404(User,pk=id),
        }
        return render(request,'Task/assignTask.html',context)
    
    def post(self,request,id):
        mana=get_object_or_404(User,pk=request.user.id)
        form=TaskFOrm(request.POST,request.FILES)
        if form.is_valid():
            foorm=form.save(commit=False)
            today = date.today()  
            if foorm.deadline<=today:
                messages.error(request, "Invalid Assign Date. The deadline must be in the future.")
                dep=request.user.department
                context={
                        "form":TaskFOrm(request.POST,),
                        "title":"Assign Task",
                        "admi":get_object_or_404(User,pk=request.user.id),
                }
                return render(request,'Task/assignTask.html',context)
            foorm.Assigened_by=mana
            foorm.emp=get_object_or_404(User,pk=id)
            foorm.save()
            messages.success(request,"Succesfully Task Assigned")
            return redirect('home')
        print(TaskFOrm(request.POST))
        dep=request.user.department
        context={
            "form":TaskFOrm(request.POST),
            "title":"Assign Task"
        }
        messages.error(request,"Fill the Form Correcclty")
        return render(request,'Task/assignTask.html',context)
    


def open_attachment(request, task_id):
    try:
        task = get_object_or_404(Task_Assigned, id=task_id)
    except Exception:
        try:
            task= get_object_or_404(Task_Submitted,id=task_id)
        except Exception:
            try:
                task=get_object_or_404(SubTaskAssigned,id=task_id)
            except Exception:
                task=get_object_or_404(SubTaskSubmit,id=task_id)

    if not task.Attachments:
        return HttpResponse("No attachment available.", content_type="text/plain")

    file_path = task.Attachments.path
    file_name = task.Attachments.name
    file_type, encoding = mimetypes.guess_type(file_path)

    if file_type is None:
        file_type = "application/octet-stream"  # Fallback for unknown file types

    # Open PDF and images in browser, force Word to download
    if file_type in ["application/pdf", "image/png", "image/jpeg"]:
        return FileResponse(open(file_path, "rb"), content_type=file_type)
    
    elif file_type in ["application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
        response = FileResponse(open(file_path, "rb"), content_type=file_type)
        response["Content-Disposition"] = f'attachment; filename="{file_name}"'
        return response
    
    # Default response for other file types
    return HttpResponse("Unsupported file format.", content_type="text/plain")




@login_required
def pending_task(request):
    if request.user.role.RoleName == "Employee" or request.user.role.RoleName == "Team Leader" :
        if Task_Assigned.objects.filter(emp=request.user,status__in=["pending","In Progress"]).exists():
            context = {
                "Tas": Task_Assigned.objects.filter(emp=request.user,status__in=["pending", "In Progress"]),
                'title': "Pending Task",
            }
            return render(request, 'Task/task.html', context)
        messages.error(request,'No Pending Task')
        return redirect('home')
    
    messages.error(request, 'Not authorized')
    return redirect('home')

@login_required
def total_tak(request):
    if request.user.role.RoleName=="admin" or request.user.is_superuser:
        Task = Task_Assigned.objects.annotate(pending_first=Case(When(status="pending", then=Value(0)), output_field=IntegerField(),)).order_by('pending_first', '-given_on')
        for i in Task:
            if Task_Submitted.objects.filter(Task=i).exists():
                t=Task_Submitted.objects.get(Task=i)
                i.Task_sub=t.status
                i.save()
            else:
                i.Task_sub="Not Submited"
                i.save()
                
        context={
            'Tas':Task,
            'title':"All-Task",
            'optiondepart': Department.objects.all().values_list('dept_name'),
        }
        return render(request,'Task/task.html',context)
    
    elif request.user.role.RoleName=="Manager":
        Task=Task_Assigned.objects.filter(Assigened_by=request.user)
        for i in Task:
            if Task_Submitted.objects.filter(Task=i).exists():
                t=Task_Submitted.objects.get(Task=i)
                i.Task_sub=t.status
                i.save()
            else:
                i.Task_sub="Not Submited"
                i.save()
                
        context={
            'Tas':Task,
            'title':"All-Task",

        }
        return render(request,'Task/task.html',context)
        
    elif request.user.role.RoleName=="Employee" or request.user.role.RoleName=="Team Leader":
        context={
            'Tas':Task_Assigned.objects.filter(emp=request.user),
            'title':"All-Task",      
        }
        return render(request,'Task/task.html',context)
    
    messages.error(request,'Not Authorize to access this page')
    return redirect('home')


@login_required
def accept_task(request,id):
    try:
        task=get_object_or_404(Task_Assigned,pk=id)
        if task:
            task.status="In Progress"
            task.save()
            messages.success(request,"Now Your Task Has been Started")
            return redirect('All_task')
    except :
        task=get_object_or_404(TeamTaskAssign,pk=id)
        if task:
            task.status="In Progress"
            task.save()
            messages.success(request,"Now Your Task Has been Started")
            return redirect('allTeamAssTask')
        messages.error(request,"No Task Avalaible")
        return render('home')
    

class Submit_task(View):
    def get(self,request,i):
        try:
                print("finding noral task manager-emp")
                task=get_object_or_404(Task_Assigned,pk=i)
                if task:
                    if task.deadline<date.today():
                        messages.error(request, "Cannot submit task now. Your deadline has exceeded.")
                        return redirect('All_task')
                    
                    if request.user.role.RoleName in ["Employee" ,'Team Leader']:
                        print(task.Attachments)
                        context={
                            'task':task,
                            'form':SubmitForm(),
                        }
                        return render(request,'Task/submitTask.html',context)
                    messages.error(request,'Not aUAthorize ')
                    return redirect('home')
                messages.error(request,'Invalid Task')
                return redirect('All_task')

        except Exception:
                print("finaidn Team Task Manager-Team Leader")
                task=get_object_or_404(TeamTaskAssign,pk=i)
                if task:
                    if task.deadline<date.today():
                        messages.error(request, "Cannot submit task now. Your deadline has exceeded.")
                        return redirect('All_task')
                    if request.user.role.RoleName=="Team Leader":
                        print(task.Attachments)
                        context={
                            'task':task,
                            'form':TeamTaskSubmitForm(),
                            'team':"hi",
                        }
                        return render(request,'Task/submitTask.html',context)
                    messages.error(request,'Not aUAthorize ')
                    return redirect('home')
                messages.error(request,'Invalid Task')
                return redirect('allTeamAssTask')
            
    def post(self,request,i):
        task=False
        team=False
        try:
            print('here to find task')
            task=get_object_or_404(Task_Assigned,pk=i)
            form=SubmitForm(request.POST,request.FILES)
            print("Normmal taksk Foujnd")
        except:
            print('here to find Team Rask')
            team=get_object_or_404(TeamTaskAssign,pk=i)
            teamTaskform=TeamTaskSubmitForm(request.POST,request.FILES)
            print("Normmal Team taksk Foujnd")

        if task:
            if form.is_valid():
                Task_detail=form.save(commit=False)
                Task_detail.Task=task
                Task_detail.emp=request.user
                Task_detail.save()
                task.status='submited'
                task.save()
                messages.success(request,'Sucesffully Submited Task')
                return redirect('All_task')
            context={
                    'task':task,
                    'form':form(),
                }
            return render(request,'Task/submitTask.html',context)
        
        if team:
            if teamTaskform.is_valid():
                Task_detail=teamTaskform.save(commit=False)
                Task_detail.Task=team
                Task_detail.submitted_by=request.user
                Task_detail.save()
                team.status='submited'
                team.save()
                messages.success(request,'Sucesffully Submited Team Task')
                return redirect('allTeamAssTask')
            context={
                    'task':task,
                    'form':teamTaskform(),
                    'team':"hi",
                }
            return render(request,'Task/submitTask.html',context)
        
def view_Assign_Task(request,pk):
    try:
        task=get_object_or_404(Task_Assigned,id=pk)
        context={
            'task':task,
        }
        print(task.Task)
        return render(request,'Task/View_assign_Task.html',context)
    except Exception:
        try:
            print("i am here trying to found team task")
            task=get_object_or_404(TeamTaskAssign,id=pk)
            print('team task foundds')
            context={
            'task':task,
            }
            print(task)
            return render(request,'Task/ViewTeamTaskAss.html',context)
        except Exception:
            messages.error(request,'No Task Assigned found')
            return redirect('home')

def View_Team_uploaded_task(request,pk):
    try:
        print('hi')
        print(pk)
        task=get_object_or_404(TeamTaskSubmitted,Task__id=pk)
        context={
            'task':task,
        }
        print('hi got it')
        return render(request,'Task/ViewTeamSubTask.html',context)
    except Exception as e:
        try:
            print('hi i am in second')
            task=get_object_or_404(TeamTaskSubmitted,id=pk)
            context={
                'task':task,
            }
            print(task)
            return render(request,'Task/ViewTeamSubTask.html',context)
        except Exception as e:
            print(e)
            print("hello ia am here")
            messages.error(request,"No Task Submitted")
            return redirect('All_task')

def View_uploaded_task(request,pk):
    try:
        print('hi')
        task=get_object_or_404(Task_Submitted,Task__id=pk)
        context={
            'task':task,
        }
        print(task.Task)
        return render(request,'Task/View_submitted_Task.html',context)
    except Exception as e:
        try:
            print('hi i am in second')
            task=get_object_or_404(Task_Submitted,id=pk)
            context={
                'task':task,
            }
            print(task)
            return render(request,'Task/View_submitted_Task.html',context)
        except Exception as e:
            print(e)
            print("hello ia am here")
            messages.error(request,"No Task Submitted")
            return redirect('All_task')

@login_required
def manager_decision_Task(request):
    manager=request.user
    task=Task_Submitted.objects.filter(Task__Assigened_by=manager)
    context={
        'task':task,
        'title':"Your EMployees TasK",
    }
    return render(request,'Task/managerTask.html',context)

@login_required
def ApproveTask(request,pk,rating):
    if request.user.role.RoleName=="Manager":
        task=False
        Teamtask=False
        try:
            task=get_object_or_404(Task_Submitted,id=pk)
        except:
            Teamtask=get_object_or_404(TeamTaskSubmitted,id=pk)

        if task:
            print(rating)
            task.status="Approved"
            task.score=rating  
            t=Task_Assigned.objects.get(id=task.Task.id)
            t.status="complete"
            t.save()
            task.save()
            messages.success(request,f'Sucessfulyy Approved Task of {task.emp.username}  ')
            return redirect("home")

        if Teamtask:
            Teamtask.status="Approved"
            Teamtask.score=rating
            t=TeamTaskAssign.objects.get(id=Teamtask.Task.id)
            t.status="complete"
            t.save()
            Teamtask.save()
            messages.success(request,f'Sucessfulyy Approved Team Task of {t.Team.Name}  ')
            return redirect("allTeamAssTask")
        messages.error(request,"Invalid Task")
        return redirect("home")

    messages.error(request,'only Manager Can perfome this task')
    return redirect('home')

@login_required
def RejectTask(request,pk,rating):
    if request.user.role.RoleName=="Manager":
        task=False
        Teamtask=False
        try:
            task=get_object_or_404(Task_Submitted,id=pk)
        except:
            Teamtask=get_object_or_404(TeamTaskSubmitted,id=pk)
        if task:
            task.status="Rejected"
            task.score=rating
            task.save()
            return redirect("manager_view_task")
        if Teamtask:
            Teamtask.status="Rejected"
            Teamtask.save()
            return redirect("allTeamAssTask")
        messages.error(request,"Invalid Task")
        return redirect("home")
    messages.error(request,'only Manager Can perfome this task')
    return redirect('home')

@login_required
def completed_task(request):
    if request.user.role.RoleName=="admin" or request.user.is_superuser:
        Task=Task_Assigned.objects.filter(status="complete")
        for i in Task:
                i.Task_sub="Completed"
                i.save()
        context={
            'Tas':Task,
            'title':"Approved Task",
        }
        return render(request,'Task/task.html',context)
    
    elif request.user.role.RoleName=="Manager":
        Task=Task_Assigned.objects.filter(Assigened_by=request.user,status="complete")
        for i in Task:
                i.Task_sub="Completed"
                i.save()
        context={
            'Tas':Task,
            'title':"Approved Task",

        }
        return render(request,'Task/task.html',context)
    
    elif request.user.role.RoleName=="Employee" or request.user.role.RoleName == "Team Leader":
        context={
            'Tas':Task_Assigned.objects.filter(emp=request.user,status="complete"),
            'title':"Approved Task",
            
        }
        return render(request,'Task/task.html',context)
    else:
        messages.error(request,'not authorze')
        return redirect('home')
    

class Team_Task_assignment(View):
    def get(self,request,id):
        if request.user.role.RoleName !="Manager":
            messages.error(request,'Not authorize to Perfome this task')
            return redirect('home')
        context={
            "form":TeamTaskAssignForm(),
            "title":"Assign Task",
             "admi":get_object_or_404(Team,pk=id),
        }
        return render(request,'Task/assignTask.html',context)
    
    def post(self,request,id):
        mana=get_object_or_404(User,pk=request.user.id)
        form=TeamTaskAssignForm(request.POST,request.FILES)
        if form.is_valid():
            foorm=form.save(commit=False)
            foorm.Assigened_by=mana
            try:
                asignToteam=get_object_or_404(Team,pk=id)
            except Exception:
                messages.error(request,"invalid team Please try Again")
                return redirect("home")
            foorm.Team=asignToteam
            foorm.save()
            messages.success(request,f"Succesfully Task Assigned  to team {asignToteam.Name}")
            return redirect('home')
        context={
            "form":TeamTaskAssignForm(),
            "title":"Assign Task",
            "admi":get_object_or_404(Team,pk=id)
        }
        messages.error(request,"Fill the Form Correcclty")
        return render(request,'Task/assignTask.html',context)

@login_required 
def allTeamassignTask(request):
    if request.user.role.RoleName =="admin":
        try:
            task=TeamTaskAssign.objects.all()
            for i in task:
                if TeamTaskSubmitted.objects.filter(Task=i).exists():
                    t=TeamTaskSubmitted.objects.get(Task=i)
                    i.Task_sub=t.status
                    i.save()
                else:
                    i.Task_sub="Not Submited"
                    i.save()
            context={
                'Tas':task,
                'title':"All Team Tasks",
            }
            return render(request,'Task/TeamTask.html',context)
        except Exception:
            messages.info(request,"No Team Task Found")
            return redirect('home')

    elif request.user.role.RoleName =="Manager":
        try:
            task=TeamTaskAssign.objects.filter(Assigened_by=request.user)
            for i in task:
                if TeamTaskSubmitted.objects.filter(Task=i).exists():
                    t=TeamTaskSubmitted.objects.get(Task=i)
                    i.Task_sub=t.status
                    i.save()
                else:
                    i.Task_sub="Not Submited"
                    i.save()
            context={
                'Tas':task,
                'title':"All Team Tasks",
            }
            return render(request,'Task/TeamTask.html',context)
        except Exception:
            print(Exception)
            messages.info(request,"No Team Task Found")
            return redirect('home')
    
    elif request.user.role.RoleName =="Team Leader":
        try:
            task=TeamTaskAssign.objects.filter(Team__leader=request.user)
            for i in task:
                if TeamTaskSubmitted.objects.filter(Task=i).exists():
                    t=TeamTaskSubmitted.objects.get(Task=i)
                    i.Task_sub=t.status
                    i.save()
                else:
                    i.Task_sub="Not Submited"
                    i.save()
            context={
                'Tas':task,
                'title':"All Team Tasks",
            }
            return render(request,'Task/TeamTask.html',context)
        except Exception:
            messages.info(request,"No Team Task Found")
            return redirect('home')

    else:
        messages.error(request,'Not authorize to Perfome this task')
        return redirect('home')