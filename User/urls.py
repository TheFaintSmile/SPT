from django.contrib import admin
from django.urls import path

from User.views import login, postSignIn, logout

urlpatterns = [
    path('login', login, name='login'),
    path('postsignin', postSignIn, name='postsignin'),
    path('logout', logout, name='logout'),
]