from django.contrib import admin
from django.urls import path

from spt.views import login, logout, registerPeserta, registerPanitia, getArbitraryUser, getAllArbitraryPanitia, joinPanitia, updateStatus, addDivisi, updateDivisi, deleteDivisi, updateProfile, updatePassword, fetchUsersRelated

urlpatterns = [
    path('login', login, name='login'),
    path('logout', logout, name='logout'),
    path('register-peserta', registerPeserta, name='registerPeserta'),
    path('register-panitia', registerPanitia, name='registerPanitia'),
    path('get-user', getArbitraryUser, name='getUser'),
    path('get-all-panitia', getAllArbitraryPanitia, name='getAllPanitia'),
    path('join-panitia', joinPanitia, name='joinPanitia'),
    path('update-status', updateStatus, name='updateStatus'),
    path('add-divisi', addDivisi, name='addDivisi'),
    path('update-divisi', updateDivisi, name='updateDivisi'),
    path('delete-divisi', deleteDivisi, name='deleteDivisi'),
    path('update-profile', updateProfile, name='updateProfile'),
    path('ganti-kata-sandi', updatePassword, name='updatePassword'),
    path('fetch-users-related', fetchUsersRelated, name='fetchUsersRelated')
]
