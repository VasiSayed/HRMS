from .models import Department 
from django.shortcuts import render,redirect
from django.views import View
from .forms import CreateDepartmntFor,Update_departmentView
from django.contrib import messages
# Create your views here.

class Create_department(View):
    def get(self,request):
        if request.user.role.RoleName != "admin":
            if request.user.is_superuser !=True:
                messages.error(request,"Only admin Can Can Perfome THis Task")
                return redirect('home')
        context={
        "title":"Create Department",
        "form":CreateDepartmntFor(),
        "button":"Create"
        }
        return render(request,'department/form.html',context)
    
    def post(self,request):
        title="Create Department"
        form=CreateDepartmntFor(request.POST)
        if form.is_valid():
            if (request.user.is_superuser==True) or (request.user.role.RoleName == "admin"):
                name=form.cleaned_data["dept_name"]
                form.save()
                messages.success(request,f"{name} Department Created Sucessfully")
                return redirect('home')
            else:
                messages.error(request,"Only admin Can Can Perfome THis Task")
                return render(request,'base.html')
        else:
            messages.error(request,"Fill the form correctly")
            for error in form.errors:
                messages.error(request,f":{error}")
            context={
                'title':title,
                'form':form,
                "button":"Create",
            }
            return render(request,'department/form.html',context)


class updateDepartmentView(View):
    def get(self,request):
        if request.user.role.RoleName != "admin":
            if request.user.is_superuser !=True:
                messages.error(request,"Only admin Can Can Perfome THis Task")
                return redirect('home')
        context={
        "title":"Update Department",
        "form":Update_departmentView(),
        "button":"Update"
        }
        return render(request,'department/form.html',context)
    
    def post(self,request):
        form=Update_departmentView(request.POST)
        if form.is_valid():
            name=form.cleaned_data['Department_Name']
            try:
                dept=Department.objects.get(dept_name=name)
                desi=form.cleaned_data['Description']
                dept.description=desi
                dept.save()
                messages.success(request,f"{name} Department sucessfully Updated")
                return redirect('home')
                
            except Department.DoesNotExist:
                messages.error(request,f"There is no such {name} department Exister")
                messages.error(request,'Please Make Sure you Are entering Rigth Deparrtment Name')
                context={
                "title":"Update Department",
                "form":form,
                "button":"Update"
                }
                return render(request,'department/form.html',context)
                            
        else:
            context={
        "title":"Update Department",
        "form":form,
        "button":"Update"
        }
        messages.error(request,"fill the form correctly")
        return render(request,'department/form.html',context)

            

def dashboard(request):
    dept=Department.objects.filter(status=True)
    sr=0
    for i in dept:
        sr+=1
        i.sr =sr
    print(dept)
    return render(request,'base.html',{"department":dept})



# def deletedept(request,dept_id):
#     if request.user.status != "admin":
#             if request.user.is_superuser !=True:
#                 messages.error(request,"Only admin Can Can Perfome THis Task")
#                 return redirect('home')
#     try:
#         dept=Department.objects.get(dept_id=dept_id)
#         dept.status=False
#         dept.save()
#         messages.warning(request,'making department inactive will cause department inactive for the employee linked with the department, so first assign different departments to those employees and then make department inactive.')
#         return redirect('Dashboard')
#     except Department.DoesNotExist:
#         messages.error(request,"No suct Department Exist")
#         return redirect('home')
    
  

    