from django.db.models import Prefetch
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.views.generic import *
from django.db.models import Q
from django.shortcuts import render_to_response
from .models import *
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


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
    audio = Audio

    def get_queryset(self):
        self.album = get_object_or_404(Album, id=int(self.kwargs['album_id']))
        return self.audio

    def get_context_data(self, **kwargs):
        context = super(AlbumsView, self).get_context_data(**kwargs)
        self.artistas = Artista.objects.all()
        self.audios = Audio.objects.filter(albums=self.album.pk).prefetch_related('artistas')

        # self.artistas = Artista.objects.filter(audios_in = self.audios)
        # objects.prefetch_related('')

        context['album'] = self.album
        context['audios'] = self.audios
        return context


class BuscadorView(View):
    # template_name = 'homepage.html'
    def get(self, request, *args, **kwargs):
        filtro = request.GET.get('q', '')
        active_tab = "tab1"

        recientes = Audio.objects.all().order_by('-fec_entrada_audio')[:5].prefetch_related(
            Prefetch('artistas', queryset=Artista.objects.only("nom_artistico").all())).all()

        recientes_list = []
        for reciente in recientes:
            audio_item = {}
            audio_item["audio"] = reciente
            nombres = ""
            for artista in reciente.artistas.all():
                if len(nombres) > 0:
                    nombres = nombres + ", "
                nombres = nombres + artista.nom_artistico

            audio_item["artistas"] = nombres
            recientes_list.append(audio_item)

        if filtro:
            qset = (
                Q(nom_audio__icontains=filtro)  # |
                # Q(artista__nom_artistico__icontains=query)
            )
            audios = Audio.objects.prefetch_related(
                Prefetch('artistas', queryset=Artista.objects.only("nom_artistico").all())).filter(
                qset).distinct().all()

            audio_list = []
            for audio in audios:
                audio_item = {}
                audio_item["audio"] = audio
                nombres = ""
                for artista in audio.artistas.all():
                    if len(nombres) > 0:
                        nombres = nombres + ", "
                    nombres = nombres + artista.nom_artistico

                audio_item["artistas"] = nombres
                audio_list.append(audio_item)

            qset = (
                Q(nom_artistico__icontains=filtro)
            )
            artistas = Artista.objects.filter(qset).distinct()

            active_tab = "tab2"
        else:
            audio_list = []
            artistas = []
        return render(request, "homepage.html", {
            "audios": audio_list,
            "artistas": artistas,
            "filtro": filtro,
            "active_tab": active_tab,
            "audios_recientes": recientes_list
        }, )


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

        if self.request.user.is_authenticated():
            user_id = self.request.user.id
        else:
            user_id = 0
        try:
            Audio.objects.get(id=int(self.kwargs['song_id']), likes__id=user_id)
            user_like = True
        except Audio.DoesNotExist:
            user_like = False
        context['user_like'] = user_like
        return context


@csrf_exempt
def like_view(request):
    if request.is_ajax():
        song_id = request.POST.get("song_id")
        audio = Audio.objects.get(pk=song_id)
        audio.likes.add(User.objects.get(id=request.user.id))
        audio.save()
        total_likes = audio.likes.count()
        message = total_likes
    else:
        message = "ERROR"
    return HttpResponse(message)


@csrf_exempt
def unlike_view(request):
    if request.is_ajax():
        song_id = request.POST.get("song_id")
        audio = Audio.objects.get(pk=song_id)
        audio.likes.remove(User.objects.get(id=request.user.id))
        audio.save()
        total_likes = audio.likes.count()
        message = total_likes
    else:
        message = "ERROR"
    return HttpResponse(message)


def donation_view(request):
    value = request.POST.get("value")
    credit_card = request.POST.get("credit_card")
    artista_a_donar = Artista.objects.get(pk=request.POST.get("artist_to_donation"))
    donation = Donaciones(valor=value, tarjeta_credito=credit_card, artista=artista_a_donar)
    donation.save()
    messages.success(request, 'Tu donación fue recibida. ¡Gracias!')
    return HttpResponseRedirect('/user/' + request.POST.get("artist_to_donation"))
