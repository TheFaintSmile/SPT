from django.contrib import admin
from django.urls import path

from User.views import login, postSignIn

urlpatterns = [
    path('login', login, name='login'),
    path('postsignin', postSignIn, name='postsignin'),
]