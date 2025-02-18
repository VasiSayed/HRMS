from django.shortcuts import render,get_object_or_404,redirect
from users.models import User
from django.views import View
from .forms import TaskFOrm,SubmitForm
from .models import Task_Assigned,Task_Submitted
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def allemp(request):
    context={
    "emp" : User.objects.filter(role__RoleName="Employee",department=request.user.department)
    }
    print(context)
    return render(request,'Task/allEmp.html',context)


class Task_assignment(View):
    def get(self,request,id):
        context={
            "form":TaskFOrm(),
            "title":"Assign Task",
             "admi":get_object_or_404(User,pk=request.user.id),
        }
        return render(request,'Task/assignTask.html',context)
    
    def post(self,request,id):
        mana=get_object_or_404(User,pk=request.user.id)
        form=TaskFOrm(request.POST)
        if form.is_valid():
            foorm=form.save(commit=False)
            foorm.Assigened_by=mana
            foorm.emp=get_object_or_404(User,pk=id)
            foorm.save()
            messages.success(request,"Succesfully Task Assigned")
            return redirect('home')
        print(TaskFOrm(request.POST))
        dep=request.user.department
        context={
            "form":TaskFOrm(request.POST,dep=dep),
            "title":"Assign Task"
        }
        messages.error(request,"Fill the Form Correcclty")
        return render(request,'Task/assignTask.html',context)
    
@login_required
def pending_task(request):
    if request.user.role.RoleName!="Employee":
        messages.error(request,'Not Authorize to access this page')
        return redirect('home')
    if Task_Assigned.objects.filter(emp=request.user,status="pending").exists():
        context={
        "Tas":Task_Assigned.objects.filter(emp=request.user,status="pending"),
        'title':"Pending Task",
        }
        return render(request,'Task/task.html',context)
    messages.error(request,'No Pending Task')
    return redirect('home')


@login_required
def total_tak(request):
    if request.user.role.RoleName=="Manager":
        context={
            'Tas':Task_Assigned.objects.filter(Assigened_by=request.user),
            'title':"All-Task",
        }
        return render(request,'Task/task.html',context)
    if request.user.role.RoleName=="Employee":
        context={
            'Tas':Task_Assigned.objects.filter(emp=request.user),
            'title':"All-Task",      
        }
        return render(request,'Task/task.html',context)
    messages.error(request,'Not Authorize to access this page')
    return redirect('home')

@login_required
def accept_task(request,id):
    task=get_object_or_404(Task_Assigned,pk=id)
    if task:
        task.status="In Progress"
        task.save()
        messages.success(request,"Now Your Task Has been Started")
        return redirect('All_task')
    messages.error(request,"No Task Avalaible")
    return render('home')
    
class Submit_task(View):
    def get(self,request,i):
        task=get_object_or_404(Task_Assigned,pk=i)
        if task:
            print(task.Attachments)
            context={
                'task':task,
                'form':SubmitForm(),
            }
            return render(request,'Task/submitTask.html',context)
        
    def post(self,request,i):
        task=get_object_or_404(Task_Assigned,pk=i)
        form=SubmitForm(request.POST,request.FILES)
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
    
def View_uploaded_task(request,pk):
    try:
        print('hi')
        task=get_object_or_404(Task_Submitted,Task__id=pk)
        context={
            'task':task,
        }
        print(task)
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
    print(task)
    context={
        'task':task,
        'title':"Your EMployees TasK",
    }
    return render(request,'Task/managerTask.html',context)