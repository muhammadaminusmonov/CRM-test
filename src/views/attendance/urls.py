# crm/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.attendance_view, name='attendance'),
    path('group/<int:group_id>/<str:date>/', views.group_attendance_view, name='group_attendance'),
]