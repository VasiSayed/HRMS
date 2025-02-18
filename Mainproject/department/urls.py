from django.urls import path
from . import views

urlpatterns = [
    path('Create-Department/',views.Create_department.as_view() ,name='Createdepart'),
    path('Update-Department/',views.updateDepartmentView.as_view(),name="UpdateDept"),
    path('dasboard',views.dashboard,name='Dashboard'),
]