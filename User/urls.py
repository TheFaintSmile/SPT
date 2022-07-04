from django.contrib import admin
from django.urls import path, include

from User.views import daftar_panitia, daftar_peserta, login

urlpatterns = [
    path('daftar-peserta', daftar_peserta, name='daftar_peserta'),
    path('daftar-panitia', daftar_panitia, name='daftar_panitia'),
    path('login', login, name='login'),

]