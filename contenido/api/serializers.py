from rest_framework import serializers
from contenido.models import Artista

class ArtistaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Artista
        fields = ('id','nom_artistico','nom_pais','nom_ciudad', 'user')