from . import views
from django.urls import path

urlpatterns = [
    path('create-event', views.create_kepanitiaan, name='create-event'),
    path('add-divisi', views.create_divisi, name='add-divisi'),
    path('postcreatekepanitiaan', views.post_create_kepanitiaan, name='postcreatekepanitiaan'),

]