from django.urls import path
from .views import teacher

urlpatterns = [
    path('', teacher, name='teacher'),
]