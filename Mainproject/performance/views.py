from django.shortcuts import render,redirect,HttpResponse
from Task.models import Task_Assigned, Task_Submitted
from leader.models import SubTaskAssigned, SubTaskSubmit
from datetime import date
from attendance.views import Working_Days_Till_Now, Whole_month_working_days,Whole_year_working_days
from attendance.models import Attendance, Leave
from django.db.models import Sum,Count,Q
from department.models import Department
from django.contrib import messages
from users.models import User




def calculate_performance(request,emp, period='monthly'):
        today = date.today()
        if period=='yearly':
            filter_kwargs_Task_Assigned = {'deadline__year': today.year, 'given_on__year': today.year}
            filter_kwargs_Task_submit={'Task__deadline__year': today.year, 'Task__given_on__year': today.year}
            filter_kwargs_attendance={'date__year': today.year}
            filter_kwargs_Leave={'date_from__year':today.year}
            filter_kwarfs_subTaskAssign={'Assigned_on__year':today.year}
            filter_kwarfs_subTaskSubmited={'submitted_on__year':today.year}

        elif period == 'monthly':
                filter_kwargs_Task_Assigned = {'deadline__month': today.month, 'deadline__year': today.year,'given_on__month': today.month, 'given_on__year': today.year}
                filter_kwargs_Task_submit = {'Task__deadline__month': today.month, 'Task__deadline__year': today.year,'Task__given_on__month': today.month, 'Task__given_on__year': today.year}
                filter_kwargs_attendance = {'date__month': today.month, 'date__year': today.year}
                filter_kwargs_Leave = {'date_from__month': today.month, 'date_from__year': today.year} 
                filter_kwarfs_subTaskAssign = {'Assigned_on__month': today.month, 'Assigned_on__year': today.year}
                filter_kwarfs_subTaskSubmited = {'submitted_on__month': today.month, 'submitted_on__year': today.year}
        else:
            filter_kwargs_Task_Assigned = {'deadline': today, 'given_on': today}
            filter_kwargs_Task_submit={'Task__deadline': today, 'Task__given_on': today}
            filter_kwargs_attendance={'date': today}
            filter_kwargs_Leave={'date_from':today}
            filter_kwarfs_subTaskAssign={'Assigned_on':today}
            filter_kwarfs_subTaskSubmited={'submitted_on':today}

        total_Task_assign = Task_Assigned.objects.filter(**filter_kwargs_Task_Assigned, emp=emp).count()
        total_Task_sub = Task_Submitted.objects.filter(**filter_kwargs_Task_submit, emp=emp).count()
        total_Task_assign_score = total_Task_assign * 10
        total_Task_sub_score = Task_Submitted.objects.filter(**filter_kwargs_Task_submit, emp=emp).aggregate(total_score=Sum('score'))['total_score'] or 0

        total_subtask_Assign=SubTaskAssigned.objects.filter(**filter_kwarfs_subTaskAssign,emp=emp).count()
        total_subtask_submit=SubTaskSubmit.objects.filter(**filter_kwarfs_subTaskSubmited,emp=emp).count()
        total_subtask_Assign_score=total_subtask_Assign*10
        total_subtask_submit_score= SubTaskSubmit.objects.filter(**filter_kwarfs_subTaskSubmited, emp=emp).aggregate(total_score=Sum('score'))['total_score'] or 0

        total_days_till_now = Working_Days_Till_Now(emp)
        total_attendance_score = total_days_till_now * 10
        total_present_days = Attendance.objects.filter(**filter_kwargs_attendance, emp=emp, status='Present').count()
        total_half_days = Attendance.objects.filter(**filter_kwargs_attendance, emp=emp, status='Half day').count()
        present_score = (total_present_days * 10) + (total_half_days * 7)

        total_late_days = Attendance.objects.filter(**filter_kwargs_attendance, emp=emp, Remark="Late").count()
        late_score = total_late_days * -3

        total_overtime_days = Attendance.objects.filter(**filter_kwargs_attendance, emp=emp, Remark='Over Time').count()
        overtime_score = total_overtime_days * 2

        total_paid_leaves = Leave.objects.filter(**filter_kwargs_Leave, emp=emp, Leave_type="PL", status="Approved").count()
        paid_leave_score = total_paid_leaves * 10

        total_casual_leaves = Leave.objects.filter(**filter_kwargs_Leave, emp=emp, Leave_type="CL", status="Approved").count()
        casual_leave_score = total_casual_leaves * 10

        total_unpaid_leaves = Leave.objects.filter(**filter_kwargs_Leave, emp=emp, Leave_type="UL", status="Approved").count()
        unpaid_leave_deduction = 0

        total_achieved_score = (
                total_Task_sub_score + present_score + late_score +
                overtime_score + paid_leave_score + casual_leave_score + unpaid_leave_deduction+total_subtask_submit_score
            )
        total_possible_score = total_Task_assign_score + total_attendance_score+total_subtask_Assign_score

        context = {
            'total_Task_assign_score': total_Task_assign_score,  # Max possible
            'total_Task_sub_score': total_Task_sub_score,  # Achieved

            'total_attendance_score': total_attendance_score,  # Max possible
            'present_score': present_score,  # Achieved

            'total_late_days': total_late_days,
            'late_score': late_score,
            'total_overtime_days': total_overtime_days,
            'overtime_score': overtime_score,

            'total_paid_leaves': total_paid_leaves,
            'paid_leave_score': paid_leave_score,
            'total_casual_leaves': total_casual_leaves,
            'casual_leave_score': casual_leave_score,
            'total_unpaid_leaves': total_unpaid_leaves,
            'unpaid_leave_deduction': unpaid_leave_deduction,

            'total_possible_score': total_possible_score,
            'total_achieved_score': total_achieved_score,

            'total_teamtask_assign_score':total_subtask_Assign_score,
            'total_teamtask_submited_score':total_subtask_submit_score,
            'progress_percentage': (total_achieved_score / total_possible_score) * 100 if total_possible_score > 0 else 0
        }
        return context
    

def calculate_performance_dept(request,period='monthly'):
    allyear=Attendance.objects.values_list('date__year',flat=True).distinct()
    if request.user.role.RoleName == "Manager":
        employees = request.user.Manager.all()
        employee_performance = {}
        for emp in employees:
            employee_performance[emp.username] = calculate_performance(request,emp,period)
            
        sorted_performance = dict(sorted(employee_performance.items(), key=lambda item: item[1]['total_achieved_score'], reverse=True))
        context = {
            'employee_performance': sorted_performance,
            'allyears':allyear
        }
        return render(request, 'performance/sample.performance.html', context)
    
    if request.user.role.RoleName in["Employee",'Team Leader' ]:
        employees=User.objects.filter(department=request.user.department,active=True).exclude(role__RoleName="Manager")
        employee_performance = {}
        for emp in employees:
            employee_performance[emp.username] = calculate_performance(request,emp,period)
            
        sorted_performance = dict(sorted(employee_performance.items(), key=lambda item: item[1]['total_achieved_score'], reverse=True))
        context = {
            'employee_performance': sorted_performance,
            'allyears':allyear

        }
        return render(request, 'performance/sample.performance.html', context)
    
    if request.user.role.RoleName=='admin':
        employees=User.objects.filter(active=True).exclude(role__RoleName__in =[ "Manager",'admin'])
        employee_performance = {}
        for emp in employees:
            employee_performance[emp.username] = calculate_performance(request,emp,period)
            
        sorted_performance = dict(sorted(employee_performance.items(), key=lambda item: item[1]['total_achieved_score'], reverse=True))
        context = {
            'employee_performance': sorted_performance,
            'allyears':allyear

        }
        return render(request, 'performance/sample.performance.html', context)        

    messages.error(request, 'Not authorized')
    return redirect('home')














def calculate_performance_By_Year_Month(request,emp,month,year):
        today = date.today()
        todayyear=date.today().year
        if month !=0 and year != 0:
            filter_kwargs_Task_Assigned = {'deadline__year': year, 'given_on__year': year ,'deadline__month': month, 'given_on__month': month }
            filter_kwargs_Task_submit={'Task__deadline__year': year, 'Task__given_on__year':year,'Task__deadline__month': month, 'Task__given_on__month':month}
            filter_kwargs_attendance={'date__year': year,'date__month': month}
            filter_kwargs_Leave={'date_from__year':year,'date_from__month':month}
            filter_kwarfs_subTaskAssign={'Assigned_on__year':year,'Assigned_on__month':month}
            filter_kwarfs_subTaskSubmited={'submitted_on__year':year,'submitted_on__month':month}

        elif month == 0 and year == 0:
            filter_kwargs_Task_Assigned = {'deadline__year': today.year, 'given_on__year': today.year}
            filter_kwargs_Task_submit={'Task__deadline__year': today.year, 'Task__given_on__year': today.year}
            filter_kwargs_attendance={'date__year': today.year}
            filter_kwargs_Leave={'date_from__year':today.year}
            filter_kwarfs_subTaskAssign={'Assigned_on__year':today.year}
            filter_kwarfs_subTaskSubmited={'submitted_on__year':today.year}

        elif month == 0:
            filter_kwargs_Task_Assigned = {'deadline__year': year, 'given_on__year': year  }
            filter_kwargs_Task_submit={'Task__deadline__year': year, 'Task__given_on__year':year}
            filter_kwargs_attendance={'date__year': year}
            filter_kwargs_Leave={'date_from__year':year,}
            filter_kwarfs_subTaskAssign={'Assigned_on__year':year}
            filter_kwarfs_subTaskSubmited={'submitted_on__year':year}
        
        elif year == 0:
            filter_kwargs_Task_Assigned = {'deadline__year': today.year, 'given_on__year': today.year ,'deadline__month': month, 'given_on__month': month }
            filter_kwargs_Task_submit={'Task__deadline__year': today.year, 'Task__given_on__year':today.year,'Task__deadline__month': month, 'Task__given_on__month':month}
            filter_kwargs_attendance={'date__year': today.year,'date__month': month}
            filter_kwargs_Leave={'date_from__year':today.year,'date_from__month':month}
            filter_kwarfs_subTaskAssign={'Assigned_on__year':today.year,'Assigned_on__month':month}
            filter_kwarfs_subTaskSubmited={'submitted_on__year':today.year,'submitted_on__month':month}
        else:
            messages.error(request,'Invalid Selection')
            return redirect('Leadership')
        

        total_Task_assign = Task_Assigned.objects.filter(**filter_kwargs_Task_Assigned, emp=emp).count()
        total_Task_sub = Task_Submitted.objects.filter(**filter_kwargs_Task_submit, emp=emp).count()
        total_Task_assign_score = total_Task_assign * 10
        total_Task_sub_score = Task_Submitted.objects.filter(**filter_kwargs_Task_submit, emp=emp).aggregate(total_score=Sum('score'))['total_score'] or 0

        total_subtask_Assign=SubTaskAssigned.objects.filter(**filter_kwarfs_subTaskAssign,emp=emp).count()
        total_subtask_submit=SubTaskSubmit.objects.filter(**filter_kwarfs_subTaskSubmited,emp=emp).count()
        total_subtask_Assign_score=total_subtask_Assign*10
        total_subtask_submit_score= SubTaskSubmit.objects.filter(**filter_kwarfs_subTaskSubmited, emp=emp).aggregate(total_score=Sum('score'))['total_score'] or 0

        if month == 0 and year == 0:
            total_days_till_now = Working_Days_Till_Now(emp)
        elif month == 0:
            total_days_till_now=Whole_year_working_days(emp,year)
        elif year == 0:
            total_days_till_now = Whole_month_working_days(emp,todayyear,month)
        elif month !=0 and year != 0:
            total_days_till_now = Whole_month_working_days(emp,year,month)

        total_attendance_score = total_days_till_now * 10
        total_present_days = Attendance.objects.filter(**filter_kwargs_attendance, emp=emp, status='Present').count()
        total_half_days = Attendance.objects.filter(**filter_kwargs_attendance, emp=emp, status='Half day').count()
        present_score = (total_present_days * 10) + (total_half_days * 6)

        total_late_days = Attendance.objects.filter(**filter_kwargs_attendance, emp=emp, Remark="Late").count()
        late_score = total_late_days * -3

        total_overtime_days = Attendance.objects.filter(**filter_kwargs_attendance, emp=emp, Remark='Over Time').count()
        overtime_score = total_overtime_days * 2

        total_paid_leaves = Leave.objects.filter(**filter_kwargs_Leave, emp=emp, Leave_type="PL", status="Approved").count()
        paid_leave_score = total_paid_leaves * 10

        total_casual_leaves = Leave.objects.filter(**filter_kwargs_Leave, emp=emp, Leave_type="CL", status="Approved").count()
        casual_leave_score = total_casual_leaves * 10

        total_unpaid_leaves = Leave.objects.filter(**filter_kwargs_Leave, emp=emp, Leave_type="UL", status="Approved").count()
        unpaid_leave_deduction = 0

        total_achieved_score = (
                total_Task_sub_score + present_score + late_score +
                overtime_score + paid_leave_score + casual_leave_score + unpaid_leave_deduction+total_subtask_submit_score
            )
        total_possible_score =  total_attendance_score + total_subtask_Assign_score + total_Task_assign_score

        context = {
            'total_Task_assign_score': total_Task_assign_score,  # Max possible
            'total_Task_sub_score': total_Task_sub_score,  # Achieved

            'total_attendance_score': total_attendance_score,  # Max possible
            'present_score': present_score,  # Achieved

            'total_late_days': total_late_days,
            'late_score': late_score,
            'total_overtime_days': total_overtime_days,
            'overtime_score': overtime_score,

            'total_paid_leaves': total_paid_leaves,
            'paid_leave_score': paid_leave_score,
            'total_casual_leaves': total_casual_leaves,
            'casual_leave_score': casual_leave_score,
            'total_unpaid_leaves': total_unpaid_leaves,
            'unpaid_leave_deduction': unpaid_leave_deduction,

            'total_possible_score': total_possible_score,
            'total_achieved_score': total_achieved_score,

            'total_teamtask_assign_score':total_subtask_Assign_score,
            'total_teamtask_submited_score':total_subtask_submit_score,
            'progress_percentage': (total_achieved_score / total_possible_score) * 100 if total_possible_score > 0 else 0
        }
        return context
    



def calculate_performance_dept_year_nall(request,month,year):
    allyear=Attendance.objects.values_list('date__year',flat=True).distinct()
    if request.user.role.RoleName == "Manager":
        employees = request.user.Manager.all()
        employee_performance = {}
        for emp in employees:
            employee_performance[emp.username] = calculate_performance_By_Year_Month(request,emp,month,year)
            
        sorted_performance = dict(sorted(employee_performance.items(), key=lambda item: item[1]['total_achieved_score'], reverse=True))
        context = {
            'employee_performance': sorted_performance,
            'allyears':allyear
        }
        return render(request, 'performance/sample.performance.html', context)
    
    if request.user.role.RoleName in["Employee",'Team Leader' ]:
        employees=User.objects.filter(department=request.user.department,active=True).exclude(role__RoleName="Manager")
        employee_performance = {}
        for emp in employees:
            employee_performance[emp.username] = calculate_performance_By_Year_Month(request,emp,month,year)
            
        sorted_performance = dict(sorted(employee_performance.items(), key=lambda item: item[1]['total_achieved_score'], reverse=True))
        context = {
            'employee_performance': sorted_performance,
            'allyears':allyear

        }
        return render(request, 'performance/sample.performance.html', context)
    
    if request.user.role.RoleName=='admin':
        employees=User.objects.filter(active=True).exclude(role__RoleName__in =[ "Manager",'admin'])
        employee_performance = {}
        for emp in employees:
            employee_performance[emp.username] = calculate_performance_By_Year_Month(request,emp,month,year)
            
        sorted_performance = dict(sorted(employee_performance.items(), key=lambda item: item[1]['total_achieved_score'], reverse=True))
        context = {
            'employee_performance': sorted_performance,
            'allyears':allyear

        }
        return render(request, 'performance/sample.performance.html', context)        

    messages.error(request, 'Not authorized')
    return redirect('home')




