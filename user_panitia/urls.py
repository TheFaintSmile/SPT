from . import views
from django.urls import path

urlpatterns = [
    path('signup', views.signUp, name='signup'),
    path('postsignup', views.postSignUp, name='postsignup'),
    path('signin', views.signIn, name='signin'),
    path('update-data-panitia', views.update_data_panitia, name='update-data-panitia'),
    path('post-update-data-panitia', views.post_update_data_panitia, name='post-update-data-panitia')
]