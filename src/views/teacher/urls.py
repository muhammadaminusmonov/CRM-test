from django.urls import path
from .views import teacher, save_teacher, toggle_teacher_status

urlpatterns = [
    path('', teacher, name='teacher'),
    path('save/', save_teacher, name='save_teacher'),
    path('toggle_status/<int:pk>/', toggle_teacher_status, name='toggle_teacher_status'),
]