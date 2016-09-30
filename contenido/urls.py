from django.conf.urls import url, include
from . import views

app_name = 'contenido'


urlpatterns = [
    url(r'^albumes$', views.AlbumesView.as_view(), name="lista_albumes"),
    url(r'^audios$', views.AudiosView.as_view(), name="lista_audios"),
    url(r'^home$', views.BuscadorView.as_view(), name="home"),
]