from .models import Department 
from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from django.views import View
from .forms import CreateDepartmntFor,Update_departmentView
from django.contrib import messages
from users.models import User
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
                if not dept.status:  
                    messages.error(request, "This department has been shut down.")
                    return redirect('Dashboard')
                
                desi=form.cleaned_data['Description']
                week_of = form.cleaned_data.get('week_of')
                if desi:  
                    dept.description=desi
                if week_of is not None: 
                    dept.week_of = week_of
                dept.save()
                messages.success(request,f"{dept.dept_name} Department sucessfully Updated")
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




def deletedept(request,dept_id):
    if request.user.role.RoleName != "admin":
            if request.user.is_superuser !=True:
                messages.error(request,"Only admin Can Can Perfome THis Task")
                return  redirect('home')
    try:
        dept=Department.objects.get(dept_id=dept_id)
        if User.objects.filter(department=dept).exists():
            messages.warning(request,'making department inactive will cause department inactive for the employee linked with the department, so first assign different departments to those employees and then make department inactive.')
            messages.info(request,'CHoose employee where you wanna shift them')
            return redirect('Choosedept',dept_id)
        dept.status=False
        dept.save()
        messages.success(request,'Succesfully Deleted the department')
        return redirect('Dashboard')
    except Department.DoesNotExist:
        messages.error(request,"No suct Department Exist")
        return redirect('home')
    
  

def choosedept(request,id):
    if request.user.role.RoleName != "admin":
            messages.error(request,"Only admin Can Can Perfome THis Task")
            return  redirect('home')
    context={
        'department':Department.objects.filter(status=True).exclude(dept_id=id),
        'title':'Choose department',
        'fromm':id,
    }
    return render(request,'department/alldept.html',context)



def shiftEmptodept(request,fromm,too):
    dept =get_object_or_404(Department,dept_id=too)
    user_cou= User.objects.filter(department=fromm).count()
    if user_cou==0:
        messages.warning(request, "No employees found in the selected department.")
        return redirect('Dashboard')
    User.objects.filter(department=fromm).update(department=dept)
    messages.success(request, f"Successfully transferred {user_cou} employees to the {dept.dept_name} Department.")
    messages.info(request,'if you want to dlete deptmart do it now')
    return redirect('Dashboard')