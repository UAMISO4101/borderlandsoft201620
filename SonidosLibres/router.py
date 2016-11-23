from django.conf.urls import url
from rest_framework.routers import SimpleRouter
from contenido.api.resources import *
from django.contrib.auth.decorators import login_required

router = SimpleRouter()
router.register(r'artistas', viewset=ArtistasViewSet)
router.register(r'audios', viewset=AudiosViewSet)
router.register(r'users', viewset=UsersViewSet)
router.register(r'albums', viewset=AlbumsViewSet)
router.register(r'donaciones', viewset=DonacionesViewSet)
router.register(r'permissions', viewset=PermissionsViewSet)
router.register(r'comments', viewset=ComentarioViewSet)
router.register(r'ratings', viewset=RatingsViewSet)


urlpatterns = [
    url(r'ratebyaudio/(?P<audio_id>[0-9]+)/$', RatingByAudioViewSet.as_view()),
    url(r'audio/(?P<id>[0-9]+)/$', AudioViewSet.as_view()),
    url(r'audio/(?P<pk>[0-9]+)/albums$', AgregarAAlbumViewSet.as_view({'put': 'list'}), name="actualizar_albums"),  # AgregarAAlbumViewSet.as_view({'put': 'update'})),
    url(r'audiosbyartista/(?P<artista_id>[0-9]+)/$', AudiosByArtistaViewSet.as_view()),
    url(r'artista/(?P<id>[0-9]+)/$', ArtistaViewSet.as_view()),
    url(r'comment/', login_required(ComentarioViewSet.as_view({'post': 'create'})), name="comment-create"),
    url(r'denuncia/', login_required(DenunciaViewSet.as_view({'post': 'create'})), name="denuncia-create"),
    url(r'comments-list/(?P<song_id>[0-9]+)/$', ComentariosByAudioViewSet.as_view(), name="coments_list"),
    url(r'rate/', login_required(RatingsViewSet.as_view({'post': 'create'})), name="rating-create"),
    url(r'^rate-delete/(?P<pk>\d+)', login_required(RatingsViewSet.as_view({'delete': 'delete'})), name="rating-delete"),
    url(r'ratebyuseraudio/(?P<audio_id>[0-9]+)/(?P<autor_id>[0-9]+)/$', RatingByUserAudioViewSet.as_view()),
    url(r'^audioestado-update/(?P<pk>\d+)', login_required(AudioUpdateEstadoViewSet.as_view({'put': 'update'})), name="audios_estado_update"),
]
urlpatterns += router.urls
