from django.conf.urls import url, include
from rest_framework.routers import SimpleRouter
from contenido.api.resources import ArtistaViewSet, AudioViewSet, AudiosViewSet, ArtistasViewSet, UsersViewSet, AlbumsViewSet, DonacionesViewSet, PermissionsViewSet, AudiosByArtistaViewSet

router = SimpleRouter()
router.register(r'artistas', viewset=ArtistasViewSet)
router.register(r'audios', viewset=AudiosViewSet)
router.register(r'users', viewset=UsersViewSet)
router.register(r'albums', viewset=AlbumsViewSet)
router.register(r'donaciones', viewset=DonacionesViewSet)
router.register(r'permissions', viewset=PermissionsViewSet)



urlpatterns = [
    url(r'audio/(?P<id>[0-9]+)/$', AudioViewSet.as_view()),
    url(r'audiosbyartista/(?P<artista_id>[0-9]+)/$', AudiosByArtistaViewSet.as_view()),
    url(r'artista/(?P<id>[0-9]+)/$', ArtistaViewSet.as_view()),

]
urlpatterns += router.urls
