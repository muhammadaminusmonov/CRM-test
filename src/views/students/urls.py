# students/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.students_list, name='students_list'),
    path('save/<int:pk>/', views.save_student, name='save_student'),
    path('save/', views.save_student, name='create_student'),
    path('toggle-status/<int:pk>/', views.toggle_student_status, name='toggle_student_status'),
]