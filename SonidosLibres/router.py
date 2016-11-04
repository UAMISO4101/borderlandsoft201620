from django.conf.urls import url, include
from rest_framework.routers import SimpleRouter
from contenido.api.resources import ArtistaViewSet, AudioViewSet, AudiosViewSet, ArtistasViewSet, UsersViewSet, AlbumsViewSet, DonacionesViewSet, PermissionsViewSet, AudiosByArtistaViewSet, \
    ComentarioViewSet, RatingsViewSet, ComentariosByAudioViewSet, RatingByUserAudioViewSet,RatingByAudioViewSet
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
    url(r'audiosbyartista/(?P<artista_id>[0-9]+)/$', AudiosByArtistaViewSet.as_view()),
    url(r'artista/(?P<id>[0-9]+)/$', ArtistaViewSet.as_view()),
    url(r'comment/', login_required(ComentarioViewSet.as_view({'post': 'create'})), name="comment-create"),
    url(r'comments-list/(?P<song_id>[0-9]+)/$', ComentariosByAudioViewSet.as_view(), name="coments_list"),
    url(r'rate/', login_required(RatingsViewSet.as_view({'post': 'create'})), name="rating-create"),
    url(r'^rate-delete/(?P<pk>\d+)', login_required(RatingsViewSet.as_view({'delete': 'delete'})), name="rating-delete"),
    url(r'ratebyuseraudio/(?P<audio_id>[0-9]+)/(?P<autor_id>[0-9]+)/$', RatingByUserAudioViewSet.as_view()),
]
urlpatterns += router.urls
