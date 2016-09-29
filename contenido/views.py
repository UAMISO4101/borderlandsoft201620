from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.generic import *
from .models import *

# Create your views here.

#class AlbumView(ListView):
#    template_name = 'contenido/albumes.html'
#    context_object_name = 'lista_albumes'

#    def get_queryset(self):
#        return Album.objects.all()

class AlbumesView(ListView):
    template_name = 'contenido/albumes.html'
    context_object_name = 'lista_artista_album'
    artista = Artista

    def get_queryset(self):
        self.artista = get_object_or_404(Artista, id=int(self.kwargs['artista_id']))
        return Artista_album.objects.filter(artista__pk=self.artista.pk)

    def get_context_data(self, **kwargs):
        context = super(AlbumesView, self).get_context_data(**kwargs)
        context['artista'] = self.artista
        return context