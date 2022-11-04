from . import views
from django.urls import path

urlpatterns = [
    path('create-event', views.create_kepanitiaan, name='data-kepanitiaan'),
    path('add-divisi', views.create_divisi, name='data-divisi'),

]