from . import views
from django.urls import path

urlpatterns = [
    path('signup', views.signUp, name='signup'),
    path('postsignup', views.postSignUp, name='postsignup'),
    path('signin', views.signIn, name='signin'),
]