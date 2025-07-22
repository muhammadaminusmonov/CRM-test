from django.urls import path
from . import views

urlpatterns = [
    path('', views.costs_management, name='costs_management'),
    path('save-teacher-salary/', views.save_teacher_salary, name='save_teacher_salary'),
    path('save-staff-salary/', views.save_staff_salary, name='save_staff_salary'),
    path('save-expense/', views.save_expense, name='save_expense'),
    path('delete-teacher-salary/<int:id>/', views.delete_teacher_salary, name='delete_teacher_salary'),
    path('delete-staff-salary/<int:id>/', views.delete_staff_salary, name='delete_staff_salary'),
    path('delete-expense/<int:id>/', views.delete_expense, name='delete_expense'),
]