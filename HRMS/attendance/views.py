from django.shortcuts import render,redirect
from .models import AttendanceDetails,Attendance,Leave
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime, timedelta
from django.views import View
import calendar
from datetime import date
from django.db.models import Q
from users.models import User
from department.models import Department
from django.db.models import Count
from .forms import Leaveform
from django.utils.timezone import now
# Create your views here.

AllMonth={
    1:'January',
    2:'February',
    3:'March',
    4:'April',
    5:'May',
    6:'June',
    7:'July',
    8:'August',
    9:'September',
    10:'October',
    11:'November',
    12:'December'
}

@login_required
def InAttendanceView(request):
    print(datetime.now().month)
    if request.user.role.RoleName not in ("Manager", "Team Leader", "Employee"):
        messages.error(request, "Not Authorized")
        return redirect('home')
    
    if request.user.department.WeekOff == datetime.now().weekday():
        messages.info(request,'Today Is an Holiday')
        return redirect('home')
    
    if 6 == datetime.now().weekday():
        messages.info(request,'Today Is an Sunday Toh Apni Maat ...')
        return redirect('home')

    try:
        atten = AttendanceDetails.objects.get(emp=request.user)
    except AttendanceDetails.DoesNotExist:
        messages.error(request, "User shift timing not found. Contact your superior for any queries.")
        return redirect('home')

    today_date = date.today()
    
    if Attendance.objects.filter(attendance_detail=atten, date=today_date, emp=request.user).exists():
        messages.info(request, "Your IN Attendance is already marked")
        return redirect('home')

    shift_start = atten.shiftStartTime
    print('shirt start',shift_start)
    current_time = datetime.now().time()

    earliest_time = (datetime.combine(today_date, shift_start) - timedelta(hours=1)).time()
    mid_time = (datetime.combine(today_date, shift_start) + timedelta(hours=1)).time()
    last_time = (datetime.combine(today_date, shift_start) + timedelta(hours=2)).time()
    

    if current_time > last_time:
        print("this is my",current_time)
        messages.error(request, "You cannot mark attendance this late. Please mark it closer to your shift time.")
        return redirect('home')
    
    if current_time < earliest_time:
        print("this is my",current_time)
        print(earliest_time)
        messages.error(request, "You cannot mark attendance this early. Please mark it closer to your shift time.")
        return redirect('home')

    remark = "On Time"
    if current_time > mid_time:
        remark = "Late"
        messages.info(request, "You are Late")

    Attendance.objects.create(
        attendance_detail=atten,
        emp=request.user,
        date=today_date,
        startTime=current_time,
        Remark=remark
    )

    messages.success(request, "Your Attendance has been successfully marked")
    messages.info(request, "Do not forget to mark Out Attendance, or it will be marked as half-day")
    return redirect('home')
    


@login_required
def outAttendanceView(request):
    try:
        atten = AttendanceDetails.objects.get(emp=request.user)
    except AttendanceDetails.DoesNotExist:
        messages.error(request, "Your Attendance Details are not set up. Contact your Manager.")
        return redirect('home')
    
    try:
        today_atten = Attendance.objects.get(attendance_detail=atten, emp=request.user, date=date.today())
    except Attendance.DoesNotExist:
        messages.error(request, "Your Today's IN Attendance is not marked.")
        return redirect('home')
    
    print(f'{datetime.now().date()}')
    if today_atten.endTime is not None:
        messages.error(request,'Out attendaance Alredy Marked')
        return redirect('home')

    print(timezone.localtime(),'this is my time')
    current_time = datetime.now().time()
    shift_end = atten.shiftEndTime
    overtime_limit = (datetime.combine(date.today(), shift_end) + timedelta(hours=2)).time()

    print(f'Current time is {current_time}')
    print(f'Shift end time is {shift_end}')
    print(f'Over limit time is {overtime_limit}')

    if current_time > overtime_limit:
        print(current_time , overtime_limit ,"helo too late")
        messages.error(request, "It's too late to mark Out Attendance.")
        return redirect('home')

    if current_time < shift_end:
        print(f'{current_time}, and shif end is {shift_end}')
        messages.info(request, "Your shift is not over yet.")
        return redirect('home')

    if current_time <= (datetime.combine(date.today(), shift_end) + timedelta(hours=1)).time():
        today_atten.endTime = current_time

        today_atten.save()
        messages.success(request, "Successfully marked Out Attendance")
        return redirect('home')


    if current_time <= (datetime.combine(date.today(), shift_end) + timedelta(hours=2)).time():
        today_atten.endTime = current_time

        if today_atten.Remark == "On Time":
            today_atten.Remark = "Over Time"
            messages.info(request, "Your OverTime is Marked")
        
        today_atten.status='Present'
        today_atten.save()
        messages.success(request, "Successfully marked Out Attendance")
        return redirect('home')
    
    messages.error(request,'Somethig Wrong Try Again Later Or Contact Your Manger')
    return redirect('home')



def Whole_month_working_days(emp,year,month):
    lastday=calendar.monthrange(year,month)[1]
    try:
        week_off=emp.department.WeekOff
    except:
        week_off=emp.WeekOff
    total_working_days=sum(1 for i in range(1,lastday+1,1) if date(year,month,i).weekday() not in [6,week_off] )
    return total_working_days


def Working_Days_Till_Now(emp):
    today=date.today().day
    month=date.today().month
    year=date.today().year
    print(emp.username)
    week_off=emp.department.WeekOff
    total_working_days=sum(1 for i in range(1,today+1,1) if date(year,month,i).weekday() not in [6,week_off] )
    return total_working_days


def Whole_year_working_days(emp, year):
    try:
        week_off = emp.department.WeekOff
    except AttributeError:
        week_off = emp.WeekOff
    
    total_working_days = sum(
        1 for month in range(1, 13)  
        for day in range(1, calendar.monthrange(year, month)[1] + 1)  
        if date(year, month, day).weekday() not in [6, week_off]  
    )
    
    return total_working_days


@login_required
def AttendanceDashBoard(request):
    today=datetime.today()
    if request.user.role.RoleName=="Manager":
        Total_emp=User.objects.filter(manager=request.user).count()
        Present_emp = Attendance.objects.filter(emp__manager=request.user,status='Present',date=date.today()).count()
        late_emp = Attendance.objects.filter(Remark='Late',emp__manager=request.user,date=date.today()).count()
        Half_Day_emp= Attendance.objects.filter(status='Half day',emp__manager=request.user,date=date.today()).count()
        months = Attendance.objects.values_list('date__month', flat=True).distinct()
        year=Attendance.objects.values_list('date__year',flat=True).distinct()
        lpendng=Leave.objects.filter(emp__manager=request.user,status='Pending').count()
        approved_leave_emp = Leave.objects.filter(emp__manager=request.user, status='Approved', date_from__lte=today, date_to__gte=today).values_list('emp', flat=True)
        absent_employees = User.objects.filter(manager=request.user).exclude(id__in=Attendance.objects.filter(emp__manager=request.user, date=today).values_list('emp', flat=True))
        absent_without_notice = absent_employees.exclude(id__in=approved_leave_emp)
        print(lpendng)

        context={
            'total':Total_emp,
            'Present_Emp' :Present_emp,
            'Late_emp' : late_emp,
            'half':Half_Day_emp,
            'absent_days' : Total_emp-Present_emp,
            'percentage_present':(Present_emp/Total_emp)*100,
            'months':months,
            'leavePen':lpendng,
            'abestn_no_notice':absent_without_notice,
            'yearrr':year

        }
        return render(request,'attendance/dashboard.html',context)
    
    if request.user.role.RoleName=="admin":
        Total_emp=User.objects.all().exclude(role__RoleName='admin').count()
        Present_emp = Attendance.objects.filter(status='Present',date=date.today()).count()
        late_emp = Attendance.objects.filter(Remark='Late',date=date.today()).count()
        Half_Day_emp= Attendance.objects.filter(status='Half day',date=date.today()).count()
        year=Attendance.objects.values_list('date__year',flat=True).distinct()
        dept=Department.objects.values_list('dept_name',flat=True).distinct()
        months = Attendance.objects.values_list('date__month', flat=True).distinct()
        Mlpendng=Leave.objects.filter(emp__role__RoleName='Manager',status='Pending').count()
        approved_leave_emp = Leave.objects.filter(status='Approved', date_from__lte=today, date_to__gte=today).values_list('emp', flat=True)
        absent_employees = User.objects.exclude(id__in=Attendance.objects.filter(date=today).values_list('emp', flat=True))
        absent_without_notice = absent_employees.exclude(id__in=approved_leave_emp)
        print('hiii',dept)
        context={
            'total':Total_emp,
            'Present_Emp' :Present_emp,
            'Late_emp' : late_emp,
            'half':Half_Day_emp,
            'absent_days' : Total_emp-Present_emp,
            'percentage_present':(Present_emp/Total_emp)*100,
            'dept':dept,
            'months':months,
            'mlEvae':Mlpendng,
            'abestn_no_notice':absent_without_notice,
            'yearrr':year

        }
        return render(request,'attendance/dashboard.html',context)
    
    messages.error(request,'Not Authorized')
    return redirect('home')
    



def attendenceInfo(request,str):
    if request.user.role.RoleName=="Manager":
        if str=="todayAll":
            context={
            'attendata':AttendanceDetails.objects.filter(emp__manager=request.user)
            }
            return render(request,'attendance/attendanceemp.html',context)
        if str=="todayPresent":
            context={
                'attendata': Attendance.objects.filter(emp__manager=request.user,status='Present',date=date.today())
            }
            return render(request,'attendance/attendanceemp.html',context)
        if str=="todayLate":
            context={
                'attendata': Attendance.objects.filter(emp__manager=request.user,Remark='Late',status='Present',date=date.today())
            }
            return render(request,'attendance/attendanceemp.html',context)
        if str=="todayAbsent":
            present_employees = Attendance.objects.filter(
                emp__manager=request.user,
                date=date.today(),
                status__in=['Present', 'Half day']
            ).values_list('emp', flat=True)  
            print(present_employees)
            absent_employees =AttendanceDetails.objects.filter(emp__manager=request.user).exclude(emp__in=present_employees)
            context = {
                'attendata': absent_employees
            }
            return render(request, 'attendance/attendanceemp.html', context)

    if request.user.role.RoleName == "admin":
        if str=="todayAll":
            context={
            'attendata': AttendanceDetails.objects.all()
            }
            return render(request,'attendance/attendanceemp.html',context)
        if str=="todayPresent":
            context={
                'attendata': Attendance.objects.filter(status='Present',date=date.today())
            }
            return render(request,'attendance/attendanceemp.html',context)
        if str=="todayLate":
            context={
                'attendata': Attendance.objects.filter(Remark='Late',status='Present',date=date.today())
            }
            return render(request,'attendance/attendanceemp.html',context)
        if str=="todayAbsent":
            present_employees = Attendance.objects.filter(date=date.today(), status__in=['Present','Half day']).values_list('emp', flat=True) 
            absent_employees = AttendanceDetails.objects.exclude(emp__in=present_employees)
            print(absent_employees)
            context = {
            'attendata': absent_employees
            }
            return render(request, 'attendance/attendanceemp.html', context)
        


def monthlyAttendace(request,year,month):
    if request.user.role.RoleName == "Manager":
        ye = request.GET.get('year', 23)
        print(ye)
        dept = request.user.department
        total_days = Whole_month_working_days(dept,year,month) 
        avg= Attendance.objects.filter(emp__manager=request.user, date__month=month, date__year=year).values('emp__id', 'emp__username').annotate(
            total_present=Count('id', filter=Q(status='Present')),avg_attendance=Count('id', filter=Q(status='Present')) * 100.0 / total_days)
        context={
            'avg':avg,
            'year':year,
            'month':month,
        }
        return render(request,'attendance/AvgAttendance.html',context)
    messages.error(request,'admin can acces this page')
    return redirect('home')




# # work in it sdfghjkl
# def MonthlyAttedance(request,dept,year,month):
#     if request.user.role.RoleName=="admin":
#         total_days = Whole_month_working_days(dept,year,month) 
#         avg= Attendance.objects.filter(date__month=month, date__year=year).values('emp__id', 'emp__username').annotate(
#             total_present=Count('id', filter=Q(status='Present')),avg_attendance=Count('id', filter=Q(status='Present')) * 100.0 / total_days)
#         context={
#             'avg':avg,
#             'year':year,
#             'month':month,
#         }
#         return render(request,'attendance/AvgAttendance.html',context)

        

def EmpmonthlyAtten(request,year,month,id):
    if request.user.role.RoleName == "Manager" or request.user.role.RoleName == 'admin':
        try:
            atten=Attendance.objects.filter(emp__id=id,date__year=year,date__month=month)
            context={
                'attendata':atten,
            }
            return render(request,'attendance/attendanceemp.html',context)
        except:
            messages.error(request,'Attendace Not Found FOr this month')
            return redirect('AttenDash')
    messages.error(request,'Not authorize')
    return redirect('home')
            

def dashboardbyDept(request,dept):
    if request.user.role.RoleName == "admin":
        today=datetime.today()
        try:
            dept=Department.objects.get(dept_name=dept)
            Total_emp=User.objects.filter(department=dept).count()
            Present_emp = Attendance.objects.filter(emp__department=dept,status='Present',date=date.today()).count()
            late_emp = Attendance.objects.filter(Remark='Late',emp__department=dept,date=date.today()).count()
            Half_Day_emp= Attendance.objects.filter(status='Half day',emp__department=dept,date=date.today()).count()
            dept1=Department.objects.values_list('dept_name',flat=True).values_list('dept_name',flat=True)
            months = Attendance.objects.values_list('date__month', flat=True).distinct()
            approved_leave_emp = Leave.objects.filter(status='Approved', date_from__lte=today, date_to__gte=today).values_list('emp', flat=True)
            absent_employees = User.objects.filter(department__dept_name=dept).exclude(id__in=Attendance.objects.filter(emp__department__dept_name=dept, date=today).values_list('emp', flat=True))
            absent_without_notice = absent_employees.exclude(id__in=approved_leave_emp)
            for i in dept1:
                for j in i:
                    print(j)
            context={
                'total':Total_emp,
                'Present_Emp' :Present_emp,
                'Late_emp' : late_emp,
                'half':Half_Day_emp,
                'absent_days' : Total_emp-Present_emp,
                'percentage_present':(Present_emp/Total_emp)*100,
                'months':months,
                'dpid':dept.dept_id,
                'dpname':dept.dept_name,
                'dept':dept1,
                'abestn_no_notice':absent_without_notice,
            }
            return render(request,'attendance/dashboard.html',context)
    
        except dept.DoesNotExist :
            messages.error(request,'Invalid Department Selected')
            return redirect('AttenDash')
        
    messages.error('only admin can acces this page')
    return redirect('home')


def get_emp_bydept(request,str,depart):
    if request.user.role.RoleName == "admin":
        try:
            de=Department.objects.get(dept_id=depart)
        except:
            messages.error(request,'invalid Department')
            return redirect('home')
        
        if str=="todayAll":
            context={
            'attendata': AttendanceDetails.objects.filter(emp__department=de)
            }
            return render(request,'attendance/attendanceemp.html',context)
        if str=="todayPresent":
            context={
                'attendata': Attendance.objects.filter(emp__department=de,status='Present',date=date.today())
            }
            return render(request,'attendance/attendanceemp.html',context)
        if str=="todayLate":
            context={
                'attendata': Attendance.objects.filter(emp__department=de,Remark='Late',status='Present',date=date.today())
            }
            return render(request,'attendance/attendanceemp.html',context)
        if str == "todayAbsent":
            today = date.today()
            present = Attendance.objects.filter(emp__department=de, date=today, status__in=['Present', 'Half day']).values_list('emp', flat=True)  
            absent_employees = AttendanceDetails.objects.filter(emp__department=de).exclude(emp__in=present)
            context = {
                'attendata': absent_employees
            }
            return render(request, 'attendance/attendanceemp.html', context)

        
    messages.error(request,'Only authorized Person Can Access')
    return redirect('home')



def monthlyAttendacebydept(request,year,month,dep):
    if request.user.role.RoleName == "admin":
        dept = Department.objects.get(dept_id=dep)
        total_days = Whole_month_working_days(dept,year,month) 
        avg= Attendance.objects.filter(emp__department=dept,date__month=month, date__year=year).values('emp__id', 'emp__username').annotate(
            total_present=Count('id', filter=Q(status='Present')),avg_attendance=Count('id', filter=Q(status='Present')) * 100.0 / total_days)
        context={
            'avg':avg,
            'year':year,
            'month':month,
        }
        return render(request,'attendance/AvgAttendance.html',context)
    messages.error(request,'Manager can acces this page')
    return render('home')



class ChangeShift(View):
    def get(self,request,id):
       pass
    
    def post(self,request,id):
        try:
            atten =AttendanceDetails.objects.get(emp__id=id)
        except AttendanceDetails.DoesNotExist:
            messages.error(request,'User DOesnt Not Exist')
            return redirect('home')
        
        if request.user.role.RoleName == "manager":
            if atten.emp.manager !=  request.user:
                messages.error(request,'Not Authorize To chnage the User shift Times')
                return redirect('home')
        

class LeaveView(View):
    def get(self, request):
        if request.user.role.RoleName=="admin":
            messages.error(request,'admin cannot aplly for leave request')
            return redirect('home')
        
        form = Leaveform()
        context = {
            'form': form,
            'title': "Leave Request Form",
        }
        return render(request, 'attendance/form.html', context)

    def post(self, request):
        form =Leaveform(request.POST,request.FILES)
        if form.is_valid():
            date_from =form.cleaned_data['date_from']
            date_to =form.cleaned_data['date_to']

            if form.Leave_type == 'SL':
               sick_leaves_count = Leave.objects.filter(
                    emp=request.user, 
                    Leave_type='SL',
                    date_from__month=date.today().month
                ).count()
               if sick_leaves_count >= 3:
                    messages.error(request, "You cannot apply for more than 3 sick leaves in a month.")
                    return redirect('home')
               
            min_adate = now().date()+timedelta(days=1)  
            if date_from < min_adate:
                messages.error(request, "Leave request must be made at least 1 day in advance.")
            elif date_from > date_to:
                messages.error(request, "Start date cannot be after the end date.")
            else:
                reqest=form.save(commit=False)
                reqest.emp=request.user
                reqest.save()
                messages.success(request, "Leave request submitted successfully.")
                return redirect('home')
        context = {
            'form': form,
            'title': "Leave Request Form",
        }
        messages.error(request,'fill the fom correctly')
        return render(request, 'attendance/form.html', context)


def LeaveAll(request):
    allleabe=Leave.objects.filter(emp=request.user).order_by('date_from')
    context={
        'leave':allleabe,
    }
    return render(request,'attendance/LeaveRequest.html',context)


def othersLeaves(request):
    if request.user.role.RoleName == "admin":
        leave=Leave.objects.filter(emp__role__RoleName="Manager")
        context={
            'leave':leave,
            'admi':True
        }
        return render(request,'attendance/LeaveRequest.html',context)
    
    if request.user.role.RoleName == "Manager": 
        leave=Leave.objects.filter( Q(emp__role__RoleName="Employee") | Q(emp__role__RoleName='Team Leader'))
        context={
            'leave':leave,
            'mana':True
        }
        return render(request,'attendance/LeaveRequest.html',context) 
    messages.error(request,'Not Authorized')
    return redirect('home')


def PendingLeave(request):
    if request.user.role.RoleName == "admin":
        leave=Leave.objects.filter(emp__role__RoleName="Manager",status='Pending')
        context={
            'leave':leave,
            'admi':True
        }
        return render(request,'attendance/LeaveRequest.html',context) 
    
    if request.user.role.RoleName == "Manager": 
        leave=Leave.objects.filter( Q(emp__role__RoleName="Employee") | Q(emp__role__RoleName='Team Leader'),status='Pending')
        context={
            'leave':leave,
            'mana':True
        }
        return render(request,'attendance/LeaveRequest.html',context) 

    messages.error(request,'Not Authorized')
    return redirect('home')


def acceptleave(request,id):
    try:
        leave=Leave.objects.get(id=id)
    except:
        messages.error(request,'Invalid Leave ID')
        return redirect('AttenDash')
    role=leave.emp.role.RoleName 
    if request.user.role.RoleName == "Manager":
        if role not in ['Employee','Team Leader']:
            messages.error(request,'not authorized')
            return redirect('AttenDash')
    if request.user.role.RoleName == "admin":
        if role != 'Manager':
            messages.error(request,'not authorized')
            return redirect('AttenDash')
    leave.status='Approved'
    leave.save()
    messages.success(request,f"Succefully Accepted Leave Request of {leave.emp.username}")
    return redirect('allleaverequest')


def RejectLeave(request,id):
    try:
        leave=Leave.objects.get(id=id)
    except:
        messages.error(request,'Invalid Leave ID')
        return redirect('home')
    leave.status='Rejected'
    leave.save()
    messages.success(request,f"Succefully Rejected Leave Request of {leave.emp.username}")
    return redirect('allleaverequest')


def allLeave(request):
    if request.user.role.RoleName == "admin":     
        leave=Leave.objects.filter(emp__role__RoleName="Manager").order_by('date_from')
        context={
            'leave':leave,
            'admi':True
        }
        return render(request,'attendance/LeaveRequest.html',context) 
    
    if request.user.role.RoleName == "Manager": 
        leave=Leave.objects.filter( Q(emp__role__RoleName="Employee") | Q(emp__role__RoleName='Team Leader')).order_by('date_from')
        context={
            'leave':leave,
            'mana':True
        }
        return render(request,'attendance/LeaveRequest.html',context) 