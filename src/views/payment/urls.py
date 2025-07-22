# finance/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.payment_management, name='payment_management'),
    path('create/', views.create_payment, name='create_payment'),
    path('update/<int:pk>/', views.update_payment, name='update_payment'),
    path('delete/<int:pk>/', views.delete_payment, name='delete_payment'),
    path('toggle-status/<int:pk>/', views.toggle_payment_status, name='toggle_payment_status'),
]