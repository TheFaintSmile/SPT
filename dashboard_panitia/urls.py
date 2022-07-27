from . import views
from django.urls import path

urlpatterns = [
    path('dashboard-panitia', views.dashboard, name='dashboard-panitia'),
]