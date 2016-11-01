from django.db.models import Prefetch
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.generic import *
from django.db.models import Q
from .models import *
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from io import BytesIO
import uuid
import datetime
from django.conf import settings


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

class FollowersView(ListView):
    template_name = 'SonidosLibres/user.html'
    context_object_name = 'lista_audios'
    usuario = User

    def get_queryset(self):
        return get_object_or_404(Artista, id=int(self.kwargs['user_id']))

    def get_context_data(self, **kwargs):
        context = super(FollowersView, self).get_context_data(**kwargs)
        self.artista = get_object_or_404(Artista, id=int(self.kwargs['user_id']))
        self.followers = self.artista.seguidores.all()
        context['artist'] = self.artista
        context['followers'] = self.followers
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

@csrf_exempt
def follow_view(request):
    if request.is_ajax():
        artist_id = request.POST.get("artista_id")
        artista = Artista.objects.get(pk=artist_id)
        artista.seguidores.add(User.objects.get(id=request.user.id))
        message = "SUCCESS"
    else:
        message = "NO OK"
    return HttpResponse(message)

def donation_view(request):
    value = request.POST.get("value")
    credit_card = request.POST.get("credit_card")
    artista_a_donar = Artista.objects.get(pk=request.POST.get("artist_to_donation"))
    donation = Donaciones(valor=value, tarjeta_credito=credit_card, artista=artista_a_donar)
    donation.save()
    messages.success(request, 'Tu donación fue recibida. ¡Gracias!')
    return HttpResponseRedirect('/user/' + request.POST.get("artist_to_donation"))

def upload_song_view(request):
    song_name = request.POST.get('upload_song_name')
    song_type = request.POST.get('upload_song_type')
    song_tags = request.POST.get('upload_song_tags')
    audio_file = request.FILES['upload_song_file_file'].read()
    image_file = request.FILES['upload_song_img_file'].read()
    audio_file_name = uuid.uuid4().urn[9:]+'.mp3'
    image_file_name = uuid.uuid4().urn[9:]+'.png'
    conn = S3Connection(settings.AWS_SECRET_KEY, settings.AWS_ACCESS_SECRET_KEY)
    bucket = conn.get_bucket(settings.AWS_STORAGE_BUCKET_NAME)
    k = Key(bucket)
    k2 = Key(bucket)
    k.key = 'images/'+image_file_name
    k2.key = 'audios/'+audio_file_name
    k.set_contents_from_file(BytesIO(image_file), policy='public-read')
    k2.set_contents_from_file(BytesIO(audio_file), policy='public-read')
    audio = Audio()
    audio.nom_audio = song_name
    audio.type_audio = song_type
    audio.tags_audio = song_tags
    audio.val_recurso = 'https://s3-us-west-2.amazonaws.com/sonidoslibres/audios/'+audio_file_name
    audio.val_imagen ='https://s3-us-west-2.amazonaws.com/sonidoslibres/images/'+image_file_name
    audio.fec_entrada_audio = datetime.datetime.now()
    audio.save()
    messages.success(request, '¡El audio fue agregado exitosamente!')
    return HttpResponseRedirect('/song/'+str(audio.id))


def comentario_view(request):
    texto_comentario = request.POST.get("texto_comentario")
    audio_comentario = Audio.objects.get(pk=request.POST.get("songId"))

    comentario = Comentario(val_comentario=texto_comentario, audio=audio_comentario)
    comentario.save()
    messages.success(request, 'Tu comentario fue registrado.')

    return HttpResponseRedirect('/song/' + request.POST.get("songId"))



class ComentariosView(ListView):
    template_name = 'SonidosLibres/audio.html'
    context_object_name = 'comentarios'
    audio = Audio

    def get_queryset(self):
        self.audio = get_object_or_404(Audio, id=int(self.kwargs['song_id']))
        return self.audio

    def get_context_data(self, **kwargs):
        context = super(ComentariosView, self).get_context_data(**kwargs)
        self.comentarios = Comentario.objects.filter(audio__id=self.audio.pk).prefetch_related('')

        context['comentarios'] = self.comentarios
        return context

