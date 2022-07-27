from . import views
from django.urls import path

urlpatterns = [
    path('dashboard-peserta', views.dashboard, name='dashboard-peserta'),
]