from django.contrib import admin
from django.urls import path, include

from User.views import daftar_panitia, login

urlpatterns = [
    path('daftar-panitia', daftar_panitia, name='daftar_panitia'),
    path('login', login, name='login'),

]