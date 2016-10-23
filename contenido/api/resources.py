from rest_framework import viewsets, generics
from .serializers import ArtistaSerializer, AudioSerializer, UserSerializer, AlbumSerializer,DonacionesSerializer,PermissionsSerializer
from ..models import Artista,Audio,User,Album,Donaciones
from django.contrib.auth.models import Permission

class ArtistaViewSet(generics.ListAPIView):
    serializer_class = ArtistaSerializer

    def get_queryset(self):
        return Artista.objects.filter(pk=int(self.kwargs['id']))

class AudioViewSet(generics.ListAPIView):
    serializer_class = AudioSerializer

    def get_queryset(self):
        return Audio.objects.filter(pk=int(self.kwargs['id']))

class AudiosByArtistaViewSet(generics.ListAPIView):
    serializer_class = AudioSerializer

    def get_queryset(self):
        return Audio.objects.filter(artistas__pk=self.kwargs['artista_id'])


class AudiosViewSet(viewsets.ModelViewSet):
    queryset = Audio.objects.all()
    serializer_class = AudioSerializer

class ArtistasViewSet(viewsets.ModelViewSet):
    queryset = Artista.objects.all()
    serializer_class = ArtistaSerializer

class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class AlbumsViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

class DonacionesViewSet(viewsets.ModelViewSet):
    queryset = Donaciones.objects.all()
    serializer_class = DonacionesSerializer

class PermissionsViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionsSerializer