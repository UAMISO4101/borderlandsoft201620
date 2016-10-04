from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.generic import *
from django.db.models import Q
from django.shortcuts import render_to_response
from .models import *

# Create your views here.

class AudiosView(ListView):
    template_name = 'contenido/audios.html'
    context_object_name = 'lista_audios'
    artista = Artista

    def get_queryset(self):
        self.artista = get_object_or_404(Artista, id=int(self.kwargs['artista_id']))
        return Audio.objects.filter(artista__pk=self.artista.pk)

    def get_context_data(self, **kwargs):
        context = super(AudiosView, self).get_context_data(**kwargs)
        context['artista'] = self.artista
        return context

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
        return render_to_response("homepage.html", {
            "audios": audios,
            "artistas" : artistas,
            "filtro": filtro,
            "active_tab" : "tab2"
        })
