from django.contrib import admin
from django.urls import path

from User.views import login, post_email_verify, postSignIn, logout, email_verify

urlpatterns = [
    path('login', login, name='login'),
    path('postsignin', postSignIn, name='postsignin'),
    path('logout', logout, name='logout'),
    path('post-email-verify', post_email_verify, name='post-email-verify'),
    path('email-verify', email_verify, name='email-verify'),
]