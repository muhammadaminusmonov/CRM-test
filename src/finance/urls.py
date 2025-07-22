from django.urls import path
from .views import statistics

urlpatterns = [
    path('', statistics, name='statistics'),
]