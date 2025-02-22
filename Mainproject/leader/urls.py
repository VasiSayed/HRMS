from django.urls import path
from . import views

urlpatterns = [
    path('Choose-Team-Leader',views.choose_Leader,name="Choose_Leader"),
    path('Create-Team/<int:pk>/',views.CreateTeam.as_view(),name="Create_team"),
    path('All-Teams/',views.Allteams,name='All_teams')
    
]