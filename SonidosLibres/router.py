from django.conf.urls import url, include
from rest_framework.routers import SimpleRouter
from contenido.api.resources import ArtistaViewSet

router = SimpleRouter()



urlpatterns = [
    url(r'artista/(?P<id>[0-9]+)/$', ArtistaViewSet.as_view()),
]
urlpatterns += router.urls
