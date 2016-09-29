from django.conf.urls import url, include
from . import views

app_name = 'contenido'


urlpatterns = [
    url(r'^albumes$', views.AlbumView.as_view(), name="lista_albumes"),
    url(r'^home$', views.BuscadorView.as_view(), name="home"),
]