from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.generic import *
from django.db.models import Q
from django.shortcuts import render_to_response
from .models import *

# Create your views here.

class AlbumView(ListView):
    template_name = 'contenido/album.html'
    context_object_name = 'lista_albumes'
    queryset = Album.objects.all()
    #serializer_class = DeporteSerializer

    def get_queryset(self):
        return Album.objects.all()


class BuscadorView(View):

    def get(self, request, *args, **kwargs):
        filtro = request.GET.get('q', '')
        if filtro:
            qset = (
                Q(nom_audio__icontains=filtro) #|
                #Q(artista__nom_artistico__icontains=query)
            )
            audios = Audio.objects.filter(qset).distinct()

            qset = (
                Q(nom_artistico__icontains=filtro)
            )
            artistas = Artista.objects.filter(qset).distinct()
        else:
            audios = []
            artistas = []
        return render_to_response("contenido/busqueda.html", {
            "audios": audios,
            "artistas" : artistas,
            "filtro": filtro
        })
