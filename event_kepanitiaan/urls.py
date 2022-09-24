from . import views
from django.urls import path

urlpatterns = [
    path('1', views.data_kepanitiaan, name='data-kepanitiaan'),
    path('2', views.data_divisi, name='data-divisi'),

]