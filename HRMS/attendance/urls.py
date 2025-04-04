from django.urls import path
from . import views
urlpatterns = [
    path('start Attendence/',views.InAttendanceView,name="startAttendence"),
    path('outattendce/',views.outAttendanceView,name='outattendence'),
    path('Attendence-DashBoard/',views.AttendanceDashBoard,name='AttenDash'),
    path('Attendance-info/<str:str>/',views.attendenceInfo,name="Atteninfo"),
    path('Attendance-monthly/<int:year>/<int:month>/',views.monthlyAttendace,name='MonthlyAvg'),
    path('details-attendace-employe/<int:year>/<int:month>/<int:id>/',views.EmpmonthlyAtten,name='detailatten'),
    path('Depart-wise-attendance/<str:dept>/',views.dashboardbyDept,name='admindept_dash'),
    path('department-Employee-Information/<str:str>/<int:depart>/',views.get_emp_bydept,name="EMpbydept"),
    path('Attendance-monthly-by-dept/<int:year>/<int:month>/<int:dep>',views.monthlyAttendacebydept,name='MonthlyAvgbydept'),
    path('Leave-Request-form/',views.LeaveView.as_view(),name='Leaveform'),
    path('All-Leave-request/',views.LeaveAll,name='AllleaveRequest'),
    path('Decision-for-pending-Leave/',views.PendingLeave,name='Peningleaveaccept'),
    path('Accept-leave-request/<int:id>/',views.acceptleave,name='acceptleave'),
    path('reject-leave-request/<int:id>/',views.RejectLeave,name='rejecttleave'),
    path('all-leave/',views.allLeave,name='allleaverequest'),
]
