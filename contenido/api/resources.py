from rest_framework import viewsets, generics
from .serializers import ArtistaSerializer, AudioSerializer, UserSerializer, AlbumSerializer,DonacionesSerializer,PermissionsSerializer, ComentarioSerializer,RatingsSerializer
from ..models import Artista,Audio,User,Album,Donaciones,Comentario,Ratings
from django.contrib.auth.models import Permission
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt


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


class RatingByUserAudioViewSet(generics.ListAPIView):
    serializer_class = RatingsSerializer

    def get_queryset(self):
        return Ratings.objects.filter(audio_id=self.kwargs['audio_id']).filter(autor_id=self.kwargs['autor_id'])

class RatingByAudioViewSet(generics.ListAPIView):
    serializer_class = RatingsSerializer

    def get_queryset(self):
        return Ratings.objects.filter(audio_id=self.kwargs['audio_id'])

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

class ComentarioViewSet(viewsets.ModelViewSet):
    queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer

    def create(self, request, format=None):
        serializer = ComentarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RatingsViewSet(viewsets.ModelViewSet):
    queryset = Ratings.objects.all()
    serializer_class = RatingsSerializer

    @csrf_exempt
    def create(self, request, format=None):
        serializer = RatingsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        serializer = self.get_object()
        serializer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ComentariosByAudioViewSet(generics.ListAPIView):
    serializer_class = ComentarioSerializer

    def get_queryset(self):
        return Comentario.objects.filter(audio__id=self.kwargs['song_id']).order_by('-fec_creacion_comen')
