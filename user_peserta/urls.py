from . import views
from django.urls import path

urlpatterns = [
    path('signup', views.signUp, name='signup'),
    path('postsignup', views.postSignUp, name='postsignup'),
    path('signin', views.signIn, name='signin'),
    path('update-data-peserta', views.update_data_peserta, name='update-data-peserta'),
    path('post-update-data-peserta', views.post_update_data_peserta, name='post-update-data-peserta'),
]