from django.shortcuts import render,redirect
from users.models import User,Role
from leader.models import Team
from django.views import View
from .forms import CreateTeamFOrm
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators  import login_required
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
        return render(request,'leader/form.html',context)
                
@login_required
def Allteams(request):
    if request.user.role.RoleName=="admin" or request.user.is_superuser:
        context={
            'team':Team.objects.filter(active=True),
             'head':f"All Teams",
             'title':"Team-page"
        }
        return render(request,'leader/Team.html',context)

    elif request.user.role.RoleName=="Manager":
        context={
            'team':Team.objects.filter(Created_by=request.user,active=True),
             'head':f"All Teams Created By {request.user.username}",
             'title':"Team-page"

        }
        return render(request,'leader/Team.html',context)
    elif request.user.role.RoleName=="Team Leader":
        context={
            'team':Team.objects.filter(leader=request.user,active=True),
            'head':f"Your All Teams",
             'title':"Team-page"

        }
        return render(request,'leader/Team.html',context)
    else:
        messages.error(request,'not authorze you are emploue')
        return redirect('home')