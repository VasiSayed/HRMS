from django.urls import path
from . import views

urlpatterns = [
    path('Choose-Team-Leader/',views.choose_Leader,name="Choose_Leader"),
    path('Create-Team/<int:pk>/',views.CreateTeam.as_view(),name="Create_team"),
    path('All-Teams/',views.Allteams,name='All_teams'),
    path('All-Teams-all/',views.Nonandallteams,name='All__allteams'),
    # path('select-Team/',views.SelectTeams,name='Select_team'),
    path('select-Empolyee-to-add/<int:pk>/',views.Team__member_Emp,name="team_member_emp"),
    path('add_team_members/<int:task>/',views.add_team_members, name='add_team_members'),
    path('All-Team-Member/<int:id>/',views.ViewTeammember,name="allTeamMember"),
    path('Team-Member-Task-Assign/<int:id>/',views.AssignedSubTask.as_view(),name="AssignSubTask"),
    path('Delete-Team/<int:id>/',views.deleteTeam , name="DeleteTeamurl"),
    path('Pending-TeamMembers-Assigned-Tak/',views.PendingSubTaskAssign,name="PendingsubTaskAss"),
    path('All-TeamMembers-Assigned-Tak/',views.AllSubTaskAssign,name="AllsubTaskAss"),
    path('Accept-sub-team-task/<int:id>/',views.accept_Team_Sub_task,name="Start_team_sub_task"),
    path("Submit-Team-Sub-Task/<int:i>/",views.Team_Sub_Submit_task.as_view(),name="Sub_submit_tadk"),
    path('View_Sub_ass_Task/<int:pk>/',views.View_uploaded_Sub_task,name="View_sub_task_asign"),
    path('Approve_Sub_Task/<int:pk>/<int:rating>/',views.ApproveTeamSubTask,name="ApprovesubTask"),
    path('Reject_Sub_Task/<int:pk>/<int:rating>/',views.RejectTeamSubTask,name="RejectsubTask"),
    path('View_Assigned_Sub_Task/<int:pk>/',views.View_uploaded_Asign_task,name="Assigned_sub_team_task"),
]