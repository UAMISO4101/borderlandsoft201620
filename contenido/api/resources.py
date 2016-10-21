from rest_framework import viewsets, generics
from .serializers import ArtistaSerializer
from ..models import Artista

class ArtistaViewSet(generics.ListAPIView):
    serializer_class = ArtistaSerializer

    def get_queryset(self):
        return Artista.objects.filter(pk=int(self.kwargs['id']))

