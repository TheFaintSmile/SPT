from django.contrib import admin
from django.urls import path, include

from User.views import daftar_panitia, daftar_peserta, login_panitia, login_peserta

urlpatterns = [
    path('daftar-peserta', daftar_peserta, name='daftar_peserta'),
    path('daftar-panitia', daftar_panitia, name='daftar_panitia'),
    path('login-panitia', login_panitia, name='login_panitia'),
    path('login-peserta', login_peserta, name='login_peserta'),

]