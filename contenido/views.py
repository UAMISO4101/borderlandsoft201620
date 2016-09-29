from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.generic import *
from .models import *

# Create your views here.

class AlbumView(ListView):
    template_name = 'contenido/album.html'
    context_object_name = 'lista_albumes'
    queryset = Album.objects.all()
    #serializer_class = DeporteSerializer

    def get_queryset(self):
        return Album.objects.all()
