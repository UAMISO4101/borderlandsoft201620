from django.conf.urls import url, include
from . import views

app_name = 'contenido'


urlpatterns = [
    url(r'^$', views.AlbumesView.as_view(), name='index'),
    url(r'^albumes/(?P<artista_id>[0-9]+)/$', views.AlbumesView.as_view(), name='album'),
    #url(r'^albumes$', views.AlbumView.as_view(), name="lista_albumes"),
]