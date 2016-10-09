"""SonidosLibres URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from contenido import views

urlpatterns = [
    url(r'^$', views.BuscadorView.as_view(), name="homepage"),
    url(r'^404/', TemplateView.as_view(template_name='404.html'), name="homepage"),
    url(r'^login/', TemplateView.as_view(template_name='login.html'), name="homepage"),
    url(r'^register/', TemplateView.as_view(template_name='register.html'), name="homepage"),
    # url(r'^audio/', TemplateView.as_view(template_name='audio.html'), name="homepage"),
    # url(r'^user/(?P<user_id>[0-9]+)/$', views.AudiosView.as_view(template_name='user.html'), name="homepage"),
    url(r'^user/(?P<user_id>[0-9]+)/$', views.AudiosView.as_view(template_name='user.html'), name='user'),
    url(r'^album/(?P<user_id>[0-9]+)/$', views.AudiosView.as_view(template_name='album.html'), name='user'),
    # url(r'^front/', include('fronttemplates.urls')),
    # url(r'', include('contenido.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^donation/', views.donation_view, name="donation"),
    url(r'^song/(?P<song_id>[0-9]+)/$', views.SongView.as_view(), name='song'),
]
