# staff/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.staff_list, name='staff_list'),
    path('save/<int:pk>/', views.save_staff, name='save_staff'),
    path('save/', views.save_staff, name='create_staff'),
    path('toggle-status/<int:pk>/', views.toggle_staff_status, name='toggle_staff_status'),
]