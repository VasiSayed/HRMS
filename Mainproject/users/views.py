from django.shortcuts import render,redirect
from users.forms import Registerform,loginform,RegisterManagerform
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import User,Role
from attendance.models import AttendanceDetails


class RegisterView(LoginRequiredMixin,View):
    login_url='login'
    def get(self,request):
        if request.user.role.RoleName not in ("admin","Manager"):
            messages.error(request,"Only Admin or manager can Create New accounts")
            return redirect('home')
        if request.user.role.RoleName=="Manager":
            context={
            'form': Registerform(),
            'title':"Register Form",
            'button':"Register",
            }
            return render(request,'users/form.html',context)
        if request.user.role.RoleName=="admin" or request.user.is_superuser:
            context={
                'form': RegisterManagerform(),
                'title':"Register Form",
                'button':"Register",
            }
            return render(request,'users/form.html',context)
    
    def post(self,request):
        if request.user.role.RoleName not in ("admin","Manager"):
            messages.error(request,"Only Admin or manager can Create New accounts")
            return redirect('home')
        
        if request.user.role.RoleName=="admin" or request.user.is_superuser:
            form=RegisterManagerform(request.POST)
        if request.user.role.RoleName=="Manager":
            form=Registerform(request.POST)

        if form.is_valid():
            user=form.save(commit=False)
            shift_start = form.cleaned_data.get('shiftStartTime')
            shift_end = form.cleaned_data.get('shiftEndTime')
            if request.user.role.RoleName=="admin" or request.user.is_superuser:
                user.role=Role.objects.get(RoleName="Manager")
                user.save()
                AttendanceDetails.objects.create(
                emp=user,
                dept=user.department if hasattr(user, 'department') else None,
                shiftStartTime=shift_start,
                shiftEndTime=shift_end
            )
                messages.success(request,"Sucesfully Registered")
                print('manager register')
                return redirect('home')
            if request.user.role.RoleName=="Manager":
                user.role=Role.objects.get(RoleName="Employee")
                user.department=request.user.department
                user.manager=request.user
                user.save()
                AttendanceDetails.objects.create(
                emp=user,
                dept=user.department if hasattr(user, 'department') else None,
                shiftStartTime=shift_start,
                shiftEndTime=shift_end
            )
                print('employee register')
                messages.success(request,"Sucesfully Registered")
                return redirect('home')
            logout(request)
            messages.error(request,'not authorize ')
            return redirect('home')
                
        context={
            'form': form,
            'title':"Register Form",
            'button':"Register",
        }
        messages.error(request,"Fill the form correctly")
        return render(request,'users/form.html',context)
    


class loginview(View):
    def get(self,request):
        context={
            'form': loginform(),
            'title':"Login Form",
            'button':"Login",
        }
        return render(request,'users/form.html',context)

    def post(self,request):
        form=loginform(request.POST)
        if form.is_valid():
            user=authenticate(request,
                            username=form.cleaned_data['username'],
                            password=form.cleaned_data['password']
                            )
            if user:
                    login(request,user)
                    messages.success(request,f"Dear {user.role} Sucesfully login")
                    return redirect('home')
            else:
                context={
                            'form': loginform(request.POST),
                            'title':"Login Form",
                            'button':"Login",
                        }
                messages.error(request,"Invalid Username Or password")
                return render(request,'users/form.html',context)

        context={
            'form': form,
            'title':"Login Form",
            'button':"Login",
                        }
        messages.error(request,"fill the form correclty")
        return render(request,'users/form.html',context)



def logoutView(request):
    logout(request)
    return redirect('home')


@login_required
def allUsers_foradmin(request,str):
    if request.user.role.RoleName=="Manager" and str=="Employee":
        context={
            "User":User.objects.filter(role__RoleName="Employee",department=request.user.department)
        }
        return render(request,'users/user.html',context)
    
    if str=="Manager":
        context={
            "User":User.objects.filter(role__RoleName="Manager")
        }
        return render(request,'users/user.html',context)
    if str=="Employee":
        context={
            "User":User.objects.filter(role__RoleName="Employee")
        }
        return render(request,'users/user.html',context)
    else:
        messages.error(request,"Please Try Again")
        return redirect('home')
    
@login_required
def All_manager(request):
    if request.user.role.RoleName=="admin" or request.user.is_superuser:
        context={
            'User':User.objects.filter(role__RoleName="Manager"),
            'title':"All Managers"
        }
        return render(request,'users/user.html',context)