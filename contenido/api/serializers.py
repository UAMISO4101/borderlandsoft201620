from rest_framework import serializers
from contenido.models import Artista, Audio, User, Album, Donaciones, Comentario, Ratings, Profile
from django.contrib.auth.models import Permission
from rest_framework.response import Response
from rest_framework import status
from pytz import timezone


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('__all__')


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    class Meta:
        model = User
        fields = ('__all__')


class ArtistaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artista
        fields = ('id','nom_artistico','nom_pais','nom_ciudad', 'user', 'val_imagen')


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ('id','val_imagen','nom_album','fec_creacion_album','artista')

class AudioSerializer(serializers.ModelSerializer):
    artistas = ArtistaSerializer(many=True,read_only=True)
    likes = UserSerializer(many=True,read_only=True)
    albums = AlbumSerializer(many=True,read_only=True)

    class Meta:
        model = Audio
        fields = ('id','nom_audio','val_imagen','val_recurso','fec_entrada_audio', 'likes', 'albums', 'artistas')

class DonacionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donaciones
        fields = ('id','valor','tarjeta_credito','artista')

class PermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ('__all__')

class ComentarioSerializer(serializers.ModelSerializer):
    autor = UserSerializer(many=False, read_only=True)
    fec_creacion_comen = serializers.DateTimeField(format="%B %d de %Y, %H:%M %p %Z")

    class Meta:
        model = Comentario
        fields = ('id','val_comentario','fec_creacion_comen','ind_publicado','autor')

    def create(self, validated_data):
        comentario = Comentario.objects.create(**validated_data)
        return comentario

class RatingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ratings
        fields = ('__all__')

    def create(self, validated_data):
        rating = Ratings.objects.create(**validated_data)
        return rating

