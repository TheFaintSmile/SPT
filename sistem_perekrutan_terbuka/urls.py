"""sistem_perekrutan_terbuka URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('homepage.urls')),
    path('user/', include('User.urls')),
    # path('user/', include(('User.urls', 'user'), namespace='user')),
    path('user_peserta/', include(('user_peserta.urls', 'user_peserta'), namespace='user_peserta')),
    path('user_panitia/', include(('user_panitia.urls', 'user_panitia'), namespace='user_panitia')),
    path('dashboard_panitia/', include(('dashboard_panitia.urls', 'dashboard_panitia'), namespace='dashboard_panitia')),
    path('backend/', include('backend.urls')),
    path('dashboard_peserta/', include(('dashboard_pendaftar.urls', 'dashboard_pendaftar'), namespace='dashboard_peserta')),
    
]
