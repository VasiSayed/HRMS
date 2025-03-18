from django.shortcuts import render,redirect,get_object_or_404
from users.models import User,Role
from leader.models import Team,Team_Member
from django.views import View
from .forms import CreateTeamFOrm,SubTaskAssForm,SubTask_SUbmitForm
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators  import login_required
from .models  import SubTaskAssigned,SubTaskSubmit
# Create your views here.

@login_required
def choose_Leader(request):
    if request.user.role.RoleName=="Manager":
        us= User.objects.filter(Q(role__RoleName="Employee") | Q(role__RoleName="Team Leader"),manager=request.user)
        if us.exists():
            context={
                'emp':us
            }
            return render(request,'leader/ChooseLeader.html',context)
        messages.info(request,'FIrst Create EMpolyee Then mak ea team')
        return redirect('home')
    else:
        messages.error(request,'Not authorized')
        return redirect('home')



class CreateTeam(View):
    def get(self,request,pk):
        context={
            'form':CreateTeamFOrm(),
            'title':"Creating Team",
            'button':"Create",
        }
        return render(request,'leader/form.html',context)
    
    def post(self,request,pk):
        form=CreateTeamFOrm(request.POST)
        if form.is_valid():
            Foram=form.save(commit=False)
            Foram.dept=request.user.department
            try:
                use=User.objects.get(pk=pk)
            except Exception:
                messages.error(request,'EMployee Doesnt Not exist')
                return redirect('home')
            use.role=Role.objects.get(RoleName="Team Leader")
            use.save()
            Foram.leader=use
            Foram.Created_by=request.user
            Foram.save()
            return redirect('home')
        context={
            'form':form,
            'title':"Creating Team",
            'button':"Create",
        }
        messages.error(request,'FIll the formm correctly')
        return render(request,'leader/form.html',context)
                
@login_required
def Allteams(request):
    if request.user.role.RoleName=="admin" or request.user.is_superuser:
        if Team.objects.filter(active=True).exists():
            context={
                'team':Team.objects.filter(active=True),
                'head':f"All Teams",
                'title':"Team-page"
            }
            return render(request,'leader/Team.html',context)
        messages.info(request,"No active Team Make it first")
        return redirect('home')

    elif request.user.role.RoleName=="Manager":
        if Team.objects.filter(Created_by=request.user,active=True).exists():
            context={
                'team':Team.objects.filter(Created_by=request.user,active=True),
                'head':f"All Teams Created By {request.user.username}",
                'title':"Team-page"

            }
            return render(request,'leader/Team.html',context)
        
        messages.info(request,"No active Team Make it first")
        return redirect('home')
    
    elif request.user.role.RoleName=="Team Leader":
        if Team.objects.filter(leader=request.user,active=True).exists():
            context={
                'team':Team.objects.filter(leader=request.user,active=True),
                'head':f"Your All Teams",
                'title':"Team-page",
                'add':'Yes'

            }
            return render(request,'leader/Team.html',context)
        messages.info(request,"No active Team Make it first")
        return redirect('home')
    
    else:
        messages.error(request,'not authorze you are emploue')
        return redirect('home')
    

# @login_required
# def SelectTeams(request):
#     if request.user.role.RoleName=="Team Leader":
#         context={
#             'team':Team.objects.filter(leader=request.user,active=True),
#             'head':f"All Teams",
#             'title':"All-Team-page",
#             'add':'Yes'
#         }
#         return render(request,'leader/Team.html',context)
    
@login_required
def Team__member_Emp(request,pk):
    Us=User.objects.filter(department=request.user.department,role__RoleName="Employee")
    team=Team.objects.get(id=pk)
    try:
        print("trying")
        team_member=Team_Member.objects.filter(Team=team).values_list('Emp__id')
        print(team_member)
        print("found")
        for i in Us:
            for j in team_member:
                if i.id in j:
                    print(j)
                    i.exist=True
                    i.save()
        context={
                'emp':Us,
                'task':pk
        }
        return render(request,'leader/choiceMember.html',context)
    
    except Exception:
        context={
            'emp':Us,
            'task':pk
        }
        return render(request,'leader/choiceMember.html',context)


@login_required
def add_team_members(request,task):
    if request.method == "POST":
        selected_employee_ids = request.POST.getlist("selected_employees")
        print('hi')
        print(selected_employee_ids)
        team = get_object_or_404(Team, id=task)
        print('team found')
        # Ensure only team leaders can add members
        if request.user != team.leader:
            messages.error(request,'only Team Leader can perfome this task')
            return redirect("home")  
        print("gond to check emp")
        # Add selected employees to the team
        for emp_id in selected_employee_ids:
            emp = get_object_or_404(User, id=emp_id)
            print(" emp found")
            
            # Ensure employee belongs to the same department
            if emp.role.RoleName == "Employee" and emp.department == team.dept:
                Team_Member.objects.get_or_create(Team=team, Emp=emp)
        messages.success(request,'sucesfuully aded a team')
        return redirect("home")
    else:
        messages.error(request,'Invalid Entry')
        return redirect("home")


@login_required
def ViewTeammember(request,id):
        # try:
            team=Team_Member.objects.filter(Team__id=id)
            context={
                'team':team,
                'title':"All Members",
                'Action':"Assign Task",
                'team_i':id

            }
            return render(request,'leader/TeamMember.html',context)
        # except Exception:
        #     messages.error(request,'No Team')
        #     return redirect('All_teams')


class AssignedSubTask(View):
    def get(self,request,id):
        if request.user.role.RoleName == "Team Leader":
            team=Team_Member.objects.filter(Team__id=id)
            context={
                'team':team,
                'title':"All Members",
                'Action':"Assign Task",
                'form':SubTaskAssForm(),

            }
            return render(request,'leader/AssignTaskTeam.html',context)
        messages.error(request,"Not Authorised to acces this page")
        return redirect('home')
    
    def post(self, request, id):
        form = SubTaskAssForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                Te = Team.objects.get(pk=id) 
                Team_Me = request.POST.getlist("selected_Members")
                count = len(Team_Me)

                print(f"Fetched Team: {Te}, Type: {type(Te)}")

                for i in Team_Me:
                    emp = User.objects.get(pk=i)
                    print(f"Assigning task to: {emp}")

                    foram = SubTaskAssigned(
                        title=form.cleaned_data['title'],
                        Attachments=form.cleaned_data.get('Attachments', None),
                        deadline=form.cleaned_data['deadline'],
                        emp=emp,
                        Team=Te
                    )
                    foram.save()  
                messages.success(request, f"Successfully assigned task to {count} employees in {Te.Name}")
                return redirect('home')

            except Team.DoesNotExist:
                messages.error(request, "Team not found")
            except User.DoesNotExist:
                messages.error(request, "One or more selected employees do not exist")

        return redirect('home')

   
def deleteTeam(request,id):
    team=Team.objects.get(pk=id)    
    if team:
            if Team.objects.filter(leader=team.leader,active=True).count() > 1:
                team.active=False
                team.save()
                messages.info(request,"Succefullly Deleted")
                return redirect('All_teams')
            Us=User.objects.get(pk=team.leader.id)
            Us.role=Role.objects.get(RoleName="Employee")
            team.active=False
            team.save()
            Us.save()
            messages.info(request,"Succefullly Deleted")
            return redirect('All_teams')
    messages.error(request,'Invalid Teams')
    return redirect('All_teams')
    

def AllSubTaskAssign(request):
    if request.user.role.RoleName =="Team Leader":
        team=SubTaskAssigned.objects.filter(Team__leader=request.user,Team__active=True)
        for i in team:
            if SubTaskSubmit.objects.filter(subtask=i).exists():
                t=SubTaskSubmit.objects.get(subtask=i)
                print("got t")
                print(t)
                i.Task_sub=t.status
                i.save()
            else:
                i.Task_sub="Not Submited"
                i.save()
        for i in team:
            print(i.Task_sub)
                
        context={
            'Task':team,
            'title':f"Task Assigned to Team By {request.user.username} ",
        }
        return render(request,'leader/SubTask.html',context)
    
    if request.user.role.RoleName =="Employee":
        team=SubTaskAssigned.objects.filter(emp=request.user,Team__active=True)
        context={
            'Task':team,
            'title':f"Task Assigned to You {request.user.username} Team(Team Name) ",
        }
        return render(request,'leader/SubTask.html',context)
    return redirect(request,"Not Authorize to access this page")

@login_required
def accept_Team_Sub_task(request,id):
    # try:
        task=get_object_or_404(SubTaskAssigned,pk=id)
        if task:
            task.status="In Progress"
            task.save()
            messages.success(request,"Now Your Task Has been Started")
            return redirect('AllsubTaskAss')
    # except :
    #     task=get_object_or_404(TeamTaskAssign,pk=id)
    #     if task:
    #         task.status="In Progress"
    #         task.save()
    #         messages.success(request,"Now Your Task Has been Started")
    #         return redirect('allTeamAssTask')
        messages.error(request,"No Task Avalaible")
        return render('home')

class Team_Sub_Submit_task(View):
    def get(self,request,i):
        task=get_object_or_404(SubTaskAssigned,pk=i)
        if task:
            print(task.Attachments)
            context={
                'task':task,
                'form':SubTask_SUbmitForm(),
            }
            return render(request,'leader/Submit_Sub_Task.html',context)
        
    def post(self,request,i):
        task=get_object_or_404(SubTaskAssigned,pk=i)
        form=SubTask_SUbmitForm(request.POST,request.FILES)
        if form.is_valid():
            Task_detail=form.save(commit=False)
            Task_detail.subtask=task
            Task_detail.emp=request.user
            Task_detail.save()
            task.status='submited'
            task.save()
            messages.success(request,'Sucesffully Submited Task')
            return redirect('AllsubTaskAss')
        context={
                'task':task,
                'form':form(),
            }
        return render(request,'leader/Submit_Sub_Task.html',context)


@login_required
def View_uploaded_Sub_task(request,pk):
    try:
        print('hi')
        task=get_object_or_404(SubTaskSubmit,subtask__id=pk)
        print("got")
        context={
            'task':task,
        }
        return render(request,'leader/v_Submitted_SubTask.html',context)
    except Exception as e:
        try:
            print('hi i am in second')
            task=get_object_or_404(SubTaskSubmit,id=pk)
            context={
                'task':task,
            }
            return render(request,'leader/v_Submitted_SubTask.html',context)
        except Exception as e:
                print(e)
                print("hello ia am here")
                messages.error(request,"No Task Submitted")
                return redirect('AllsubTaskAss')


def View_uploaded_Asign_task(request,pk):
                print("I am in third")
                task=get_object_or_404(SubTaskAssigned,id=pk)
                if task:
                    context={
                        'task':task,
                    }
                    print(task)
                    return render(request,'leader/v_assign_sub_task.html',context) 
                messages.error(request,"No Task Submitted")
                return redirect('AllsubTaskAss')
                  

@login_required
def ApproveTeamSubTask(request,pk):
    if request.user.role.RoleName=="Team Leader":
        task=get_object_or_404(SubTaskSubmit,id=pk)
        if task:
            task.status="Approved"
            t=SubTaskAssigned.objects.get(id=task.subtask.id)
            t.status="complete"
            t.save()
            task.save()
            return redirect("AllsubTaskAss")
        messages.error(request,"Invalid Task")
        return redirect("AllsubTaskAss")
    messages.error(request,'only Manager Can perfome this task')
    return redirect('home')

def RejectTeamSubTask(request,pk):
    if request.user.role.RoleName=="Team Leader":
        task=get_object_or_404(SubTaskSubmit,id=pk)
        if task:
            task.status="Rejected"
            task.save()
            return redirect("AllsubTaskAss")
        messages.error(request,"Invalid Task")
        return redirect("AllsubTaskAss")
    messages.error(request,'only Manager Can perfome this task')
    return redirect('home')

