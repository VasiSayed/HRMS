from django.urls import path
from . import views
urlpatterns = [
    path('All-Empolyee/',views.allemp,name="All_User"),
    path('Task-Assignment/<int:id>/',views.Task_assignment.as_view(),name="task_assign"),
    path('Pending-Task/',views.pending_task,name="Pending_task"),
    path('The-All-Task/',views.total_tak,name="All_task"),
    path('Start-Task/<int:id>/',views.accept_task,name='Start_task'),
    path('Submit-Task/<int:i>/',views.Submit_task.as_view(),name='submit_task'),
    path('Submmitted-task/',views.manager_decision_Task,name='manager_view_task'),
    path('View-uploaded-Task/<int:pk>/',views.View_uploaded_task,name='view_task'),
    path('View-Assigned-Task/<int:pk>/',views.view_Assign_Task,name='view_task_assign'),
    path('view-attachment/<int:task_id>/',views.open_attachment, name='open_attachment'),
    path('Approve-Submitted-Task/<int:pk>/<int:rating>/',views.ApproveTask,name="ap_task"),
    path('reject-Submitted-Task/<int:pk>/<int:rating>/',views.RejectTask,name="rj_task"),
    path('Completed-Task/',views.completed_task,name='comp_task'),
    path('Team-task-assign/<int:id>/',views.Team_Task_assignment.as_view(),name="Team_task_assign"),
    path('All-team-task/',views.allTeamassignTask,name="allTeamAssTask"),
    path('View-Team-Subbbbbmited-task/<int:pk>/',views.View_Team_uploaded_task,name="View_Team_Tasksub"),
]