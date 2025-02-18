from django.urls import path
from . import views
urlpatterns = [
    path('All-Empolyee/',views.allemp,name="All_User"),
    path('Task-Assignment/<int:id>/',views.Task_assignment.as_view(),name="task_assign"),
    path('Pending-Task/',views.pending_task,name="Pending_task"),
    path('The-All-Task/',views.total_tak,name="All_task"),
    path('Start-Task/<int:id>/',views.accept_task,name='Start_task'),
    path('Submit-Task/<int:i>/',views.Submit_task.as_view(),name='submit_task'),
    path('View-uploaded-Task/<int:pk>/',views.View_uploaded_task,name='view_task'),
    path('Submmitted-task/',views.manager_decision_Task,name='manager_view_task')
]