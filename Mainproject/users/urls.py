from django.urls import path
from . import views
urlpatterns = [
    path('register/',views.RegisterView.as_view(),name="register"),
    path('login/',views.loginview.as_view(),name="login"),
    path('logout/',views.logoutView,name='logout'),
    path('All/<str:str>/',views.allUsers_foradmin,name="all_userss_foradmin"),
    path('All-manager/',views.All_manager,name="all_manager"),
]