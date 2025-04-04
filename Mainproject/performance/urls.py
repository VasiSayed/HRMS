from django.urls import path
from . import views
urlpatterns = [
    path('all-employees-score/',views.calculate_performance_dept,name='Leadership'),
    path('filtered-emp-performance/<int:month>/<int:year>/',views.calculate_performance_dept_year_nall,name='modifiedperformance'),

]