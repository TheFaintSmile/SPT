from django.contrib import admin
from django.urls import include, path

from homepage.views import home, team

urlpatterns = [
    path('', home, name='home'),
    path('team', team, name='team'),

    
]
