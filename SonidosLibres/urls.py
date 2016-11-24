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
from usuarios import views as view_user
from django.contrib.auth.views import login, logout_then_login
from django.conf.urls.static import static
from .router import urlpatterns
from .settings import common
from django.contrib.auth.decorators import login_required

urlpatterns = [
                  url(r'^$', views.BuscadorView.as_view(), name="homepage"),
                  url(r'^404/', TemplateView.as_view(template_name='404.html'), name="error"),
                  # url(r'^login/', TemplateView.as_view(template_name='login.html'), name="login"),
                  url(r'^accounts/login/', login, {'template_name': 'login.html'}, name="login"),
                  url(r'^logout/', logout_then_login, name="logout"),
                  # url(r'^audio/', TemplateView.as_view(template_name='audio.html'), name="homepage"),
                  # url(r'^user/(?P<user_id>[0-9]+)/$', views.AudiosView.as_view(template_name='user.html'), name="homepage"),
                  url(r'^user/(?P<user_id>[0-9]+)/$', views.AudiosView.as_view(template_name='user.html'), name='user'),
                  url(r'^album/(?P<album_id>[0-9]+)/$', views.AlbumsView.as_view(template_name='album.html'),
                      name='album'),
                  # url(r'^front/', include('fronttemplates.urls')),
                  # url(r'', include('contenido.urls')),
                  url(r'^admin/', admin.site.urls),
                  url(r'^usuarios/', include('usuarios.urls', namespace="usuarios")),
                  url(r'^donation/', views.donation_view, name="donation"),
                  url(r'^song/(?P<song_id>[0-9]+)/$', views.SongView.as_view(), name='song'),
                  url(r'^like/', views.like_view, name='like'),
                  url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
                  url(r'^api/', include(urlpatterns)),
                  url(r'^unlike/', views.unlike_view, name='unlike'),
                  url(r'^upload/song/', views.upload_song_view, name='upload-song'),
                  url(r'^upload/album/', views.upload_album_view, name='upload-album'),
                  url(r'^comment-add/', login_required(views.comentario_view), name="comment_add"),
                  url(r'^follow/', views.follow_view, name='follow'),
                  url(r'^edit/user/(?P<pk>[0-9]+)/$', view_user.ProfileModificacion.as_view(),
                      name="editar_informacion"),
                  url(r'^edit/song/info/', views.edit_song_info_view, name="edit_song_read"),
                  url(r'^edit/song/', views.edit_song_view, name="edit_song"),
                  # Python Social Auth URLs
                  url('', include('django.contrib.auth.urls', namespace='auth')),
                  url('', include('social.apps.django_app.urls', namespace='social')),
              ] + static(common.MEDIA_URL, document_root=common.MEDIA_ROOT)
