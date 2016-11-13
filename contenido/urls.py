from django.conf.urls import url
from . import views

app_name = 'contenido'


urlpatterns = [
    url(r'^$', views.BuscadorView.as_view(), name="home"),
    url(r'^albumes$', views.AlbumesView.as_view(), name="lista_albumes"),
    url(r'^audios$', views.AudiosView.as_view(), name="lista_audios"),
    url(r'^home$', views.BuscadorView.as_view(), name="home"),
    url(r'^song/(?P<song_id>[0-9]+)/$', views.SongView.as_view(), name='song'),
]
