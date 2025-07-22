from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProfitAnalysisView.as_view(), name='profit_analysis'),
]