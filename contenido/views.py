from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.generic import *
from django.db.models import Q
from django.shortcuts import render_to_response
from .models import *
from django.http import HttpResponseRedirect
from django.contrib import messages


# Create your views here.
class ArtistaView(ListView):
    # template_name = 'SonidosLibres/user.html'
    context_object_name = 'lista_artistas'

    def get_queryset(self):
        return Audio.objects.all()


class AudiosView(ListView):
    template_name = 'SonidosLibres/user.html'
    context_object_name = 'lista_audios'
    artista = Artista

    def get_queryset(self):
        return get_object_or_404(Artista, id=int(self.kwargs['user_id']))


    def get_context_data(self, **kwargs):
        context = super(AudiosView, self).get_context_data(**kwargs)
        self.artista = get_object_or_404(Artista, id=int(self.kwargs['user_id']))
        self.albums = Album.objects.filter(artista__pk=self.artista.pk)
        self.audios = Audio.objects.filter(artistas__pk=self.artista.pk)
        context['artist'] = self.artista
        context['albums'] = self.albums
        context['audios'] = self.audios
        return context

class AlbumsView(ListView):
    template_name = 'SonidosLibres/album.html'
    context_object_name = 'audios'


    def get_queryset(self):
        self.album = get_object_or_404(Album, id=int(self.kwargs['album_id']))

        return Audio.objects.filter(albums=self.album.pk)

    #def get_context_data(self, **kwargs):
     #   context = super(AlbumsView, self).get_context_data(**kwargs)
      #  context['album'] = self.album
       # return context


class BuscadorView(View):
    def get(self, request, *args, **kwargs):
        filtro = request.GET.get('q', '')
        active_tab = "tab1"
        if filtro:
            qset = (
                Q(nom_audio__icontains=filtro)  # |
                # Q(artista__nom_artistico__icontains=query)
            )
            audios = Audio.objects.filter(qset).distinct()

            qset = (
                Q(nom_artistico__icontains=filtro)
            )
            artistas = Artista.objects.filter(qset).distinct()

            active_tab = "tab2"
        else:
            audios = []
            artistas = []

        return render_to_response("homepage.html", {
            "audios": audios,
            "artistas": artistas,
            "filtro": filtro,
            "active_tab": active_tab,
            "audios_recientes": Audio.objects.all().order_by('-fec_entrada_audio')[:5]
        })


class SongView(ListView):
    template_name = 'audio.html'
    context_object_name = 'song'
    audio = Audio

    def get_queryset(self):
        return get_object_or_404(Audio, id=int(self.kwargs['song_id']))

    def get_context_data(self, **kwargs):
        audio = Audio.objects.get(id=int(self.kwargs['song_id']))
        total_likes = audio.likes.count()
        context = super(SongView, self).get_context_data(**kwargs)
        context['total_likes'] = total_likes
        return context


def donation_view(request):
    value = request.POST.get("value")
    credit_card = request.POST.get("credit_card")
    artista_a_donar = Artista.objects.get(pk=request.POST.get("artist_to_donation"))
    donation = Donaciones(valor=value, tarjeta_credito=credit_card, artista=artista_a_donar)
    donation.save()
    messages.success(request, 'Tu donación fue recibida. ¡Gracias!')
    return HttpResponseRedirect('/user/'+request.POST.get("artist_to_donation"))
