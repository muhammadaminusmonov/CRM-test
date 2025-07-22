from django.urls import path
from . import views

urlpatterns = [
    path('', views.teacher_salary_view, name='teacher_salary'),
    path('<int:record_id>/', views.get_salary_record, name='get_salary_record'),
]