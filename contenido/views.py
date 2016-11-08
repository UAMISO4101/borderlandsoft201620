# - *- coding: utf-8 - *-

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
from django.core.mail import send_mail


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
        self.audios = Audio.objects.filter(artistas__pk=self.artista.pk).prefetch_related('artistas').all()
        if not self.artista.user is None:
            self.artistas_que_sigo = Artista.objects.filter(seguidores=self.artista.user.id)
            context['artistas_que_sigo'] = self.artistas_que_sigo

        self.audios_list = []
        for audio in self.audios:
            audio_item = {}
            audio_item["audio"] = audio
            nombres = ""
            for artista in audio.artistas.all():
                if len(nombres) > 0:
                    nombres = nombres + ", "
                nombres = nombres + artista.nom_artistico

            audio_item["artistas"] = nombres
            self.audios_list.append(audio_item)

        context['artist'] = self.artista
        context['albums'] = self.albums
        context['audios'] = self.audios
        context['audios_list'] = self.audios_list
        if self.request.user.is_authenticated():
            user_id = self.request.user.id
        else:
            user_id = 0
        try:
            Artista.objects.get(id=int(self.artista.id), seguidores__id=user_id)
            user_follow = True
        except Artista.DoesNotExist:
            user_follow = False
        context['user_follow'] = user_follow
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

        recientes = Audio.objects.all().order_by('-fec_entrada_audio')[:20].prefetch_related(
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
        artistas = audio.artistas.all()
        for artista in artistas:
            send_mail('[SonidosLibres] Notificación de contenido',
                      'Hola ' + artista.nom_artistico + '! Recibiste un like en tu contendido ' + audio.nom_audio + '!',
                      'Notifications SL <notification@sonidoslibres.com>', [artista.email])
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
        artist_id = request.POST.get("artist_id")
        artista = Artista.objects.get(pk=artist_id)
        artista.seguidores.add(User.objects.get(id=request.user.id))
        artista.save()
        total_followers = artista.seguidores.count()
        message = total_followers
        send_mail('[SonidosLibres] Notificación de contenido',
                  '!Enhorabuena ' + artista.nom_artistico + '! Un nuevo usuario te esta siguiendo.',
                  'Notifications SL <notification@sonidoslibres.com>', [artista.email])
    else:
        message = "ERROR"
    return HttpResponse(message)


@csrf_exempt
def unfollow_view(request):
    if request.is_ajax():
        artist_id = request.POST.get("artista_id")
        artista = Artista.objects.get(pk=artist_id)
        try:
            artista.seguidores.remove(User.objects.get(id=request.user.id))
            message = "SUCCESS"
            return HttpResponse(message)
        except:
            message = "NO OK"
            return HttpResponse(message)
    else:
        message = "NO OK"
    return HttpResponse(message)


@csrf_exempt
def is_follower_view(request):
    if request.is_ajax():
        if request.user.is_authenticated():
            current_user = request.user.id
            user_id = request.POST.get("user_id")
            artista = Artista.objects.get(user=current_user)
            if artista.seguidores.filter(user__pk=user_id).count() > 0:
                message = True
                return HttpResponse(message)

    message = False
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
    audio_file_name = uuid.uuid4().urn[9:] + '.mp3'
    image_file_name = uuid.uuid4().urn[9:] + '.png'
    conn = S3Connection(settings.AWS_SECRET_KEY, settings.AWS_ACCESS_SECRET_KEY)
    bucket = conn.get_bucket(settings.AWS_STORAGE_BUCKET_NAME)
    k = Key(bucket)
    k2 = Key(bucket)
    k.key = 'images/' + image_file_name
    k2.key = 'audios/' + audio_file_name
    k.set_contents_from_file(BytesIO(image_file), policy='public-read')
    k2.set_contents_from_file(BytesIO(audio_file), policy='public-read')
    audio = Audio()
    audio.nom_audio = song_name
    audio.type_audio = song_type
    audio.tags_audio = song_tags
    audio.val_recurso = 'https://s3-us-west-2.amazonaws.com/sonidoslibres/audios/' + audio_file_name
    audio.val_imagen = 'https://s3-us-west-2.amazonaws.com/sonidoslibres/images/' + image_file_name
    audio.fec_entrada_audio = datetime.datetime.now()
    audio.save()
    messages.success(request, '¡El audio fue agregado exitosamente!')
    return HttpResponseRedirect('/song/' + str(audio.id))


def upload_album_view(request):
    # Data from template
    album_name = request.POST.get('upload_album_name')
    album_year = request.POST.get('upload_album_year')
    image_file = request.FILES['upload_album_img_file'].read()
    artista = Artista.objects.get(user=request.user)
    image_file_name = uuid.uuid4().urn[9:] + '.png'

    # S3
    conn = S3Connection(settings.AWS_SECRET_KEY, settings.AWS_ACCESS_SECRET_KEY)
    bucket = conn.get_bucket(settings.AWS_STORAGE_BUCKET_NAME)
    k = Key(bucket)
    k.key = 'images/' + image_file_name
    k.set_contents_from_file(BytesIO(image_file), policy='public-read')

    # Model
    album = Album()
    album.nom_album = album_name
    album.val_imagen = 'https://s3-us-west-2.amazonaws.com/sonidoslibres/images/' + image_file_name
    album.fec_creacion_album = datetime.datetime(int(album_year), 1, 1, 0, 0)
    album.artista = artista
    album.save()

    messages.success(request, '¡El album fue agregado exitosamente!')
    return HttpResponseRedirect('/album/' + str(album.id))


def comentario_view(request):
    texto_comentario = request.POST.get("texto_comentario")
    audio_comentario = Audio.objects.get(pk=request.POST.get("songId"))
    autor_comentario = User.objects.get(pk=request.POST.get("userId"))

    comentario = Comentario(val_comentario=texto_comentario, audio=audio_comentario, autor=autor_comentario)
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
        self.comentarios = Comentario.objects.filter(audio__id=self.audio.pk).prefetch_related('autor').all()

        context['comentarios'] = self.comentarios
        return context


def update_user_social_data(request, *args, **kwargs):
    user = kwargs['user']
    if not kwargs['is_new']:
        return
    user = kwargs['user']
    if kwargs['backend'].__class__.__name__ == 'FacebookBackend':
        fbuid = kwargs['response']['id']
        access_token = kwargs['response']['access_token']

        url = 'https://graph.facebook.com/{0}/' \
              '?fields=email,gender,name' \
              '&access_token={1}'.format(fbuid, access_token, )

        photo_url = "http://graph.facebook.com/%s/picture?type=large" \
                    % kwargs['response']['id']
        request = urllib2.Request(url)
        response = urllib2.urlopen(request).read()
        email = json.loads(response).get('email')
        name = json.loads(response).get('name')
        gender = json.loads(response).get('gender')
