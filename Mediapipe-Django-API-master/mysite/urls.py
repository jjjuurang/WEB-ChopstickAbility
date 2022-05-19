"""mysite URL Configuration

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
from os import name
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from mysite.core import views

urlpatterns = [

    path('', auth_views.LoginView.as_view(template_name='firstmain.html'), name='firstmain'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),

    path('guide/', views.guide, name='guide'),
    path('home/', views.Home.as_view(), name='home'),

    # four links according to the four bottons
    path('image_upload/', views.image_upload_view, name='image_upload'),
    path('video_input/', views.video_input, name='video_input'),
    path('video_input01/', views.video_input01, name='video_input01'),
    path('video_input02/', views.video_input02, name='video_input02'),
    path('video_input03/', views.video_input03, name='video_input03'),

    path('video_input/video_stream1', views.video_stream1, name='video_input/video_stream1'),
    path('video_input/video_stream2', views.video_stream2, name='video_input/video_stream2'),
    path('video_input/video_stream3', views.video_stream3, name='video_input/video_stream3'),
    path('video_input/video_stream4', views.video_stream4, name='video_input/video_stream4'),
    path('video_input/video_save', views.video_save, name='video_input/video_save'),

    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
