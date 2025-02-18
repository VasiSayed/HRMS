from django.shortcuts import render,redirect
from users.forms import Registerform,loginform
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import User


class RegisterView(LoginRequiredMixin,View):
    login_url='login'
    def get(self,request):
        if request.user.role.RoleName not in ("admin","Manager"):
            messages.error(request,"Only Admin or manager can Create New accounts")
            return redirect('home')
        if request.user.role.RoleName=="Manager":
            context={
            'form': Registerform(role=request.user.role.RoleName),
            'title':"Register Form",
            'button':"Register",
            }
            return render(request,'users/form.html',context)
        context={
            'form': Registerform(),
            'title':"Register Form",
            'button':"Register",
        }
        return render(request,'users/form.html',context)
    
    def post(self,request):
        if request.user.role.RoleName not in ("admin","Manager"):
            messages.error(request,"Only Admin or manager can Create New accounts")
            return redirect('home')
        form=Registerform(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.save()
            messages.success(request,"Sucesfully Registered")
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
    # if str=="admin":
    #     context={
    #         "User":User.objects.filter(role__RoleName="admin")
    #     }
    #     return render(request,'users/user.html',context)
    else:
        messages.error(request,"Please Try Again")
        return redirect('home')
    