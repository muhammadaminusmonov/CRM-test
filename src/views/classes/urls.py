# crm/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.classes_view, name='classes'),
    path('add/', views.add_class_view, name='add_class'),
    path('edit/<int:class_id>/', views.edit_class_view, name='edit_class'),
    path('toggle-status/<int:class_id>/', views.toggle_class_status, name='toggle_class_status'),
]