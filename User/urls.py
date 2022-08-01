from turtle import update
from django.contrib import admin
from django.urls import path

from User.views import login, post_email_verify, postSignIn, logout, email_verify, change_password, update_data

urlpatterns = [
    path('login', login, name='login'),
    path('postsignin', postSignIn, name='postsignin'),
    path('logout', logout, name='logout'),
    path('post-email-verify', post_email_verify, name='post-email-verify'),
    path('email-verify', email_verify, name='email-verify'),
    path('change-password', change_password, name='change-password'),
    path('update', update_data, name='update-data'),


]