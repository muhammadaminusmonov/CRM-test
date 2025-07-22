# finance/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.expense_management, name='expense_management'),
    path('create/', views.create_expense, name='create_expense'),
    path('update/<int:pk>/', views.update_expense, name='update_expense'),
    path('delete/<int:pk>/', views.delete_expense, name='delete_expense'),
    path('toggle-status/<int:pk>/', views.toggle_status, name='toggle_status'),
]