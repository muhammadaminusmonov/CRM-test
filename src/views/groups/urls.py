from django.urls import path
from . import views

urlpatterns = [
    path('', views.group_management, name='group_management'),
    path('save-group/', views.save_group, name='save_group'),
    path('delete-group/<int:group_id>/', views.delete_group, name='delete_group'),
    path('add-student/<int:group_id>/', views.add_student_to_group, name='add_student_to_group'),
    path('remove-student/<int:group_id>/<int:student_id>/', views.remove_student_from_group, name='remove_student_from_group'),
]