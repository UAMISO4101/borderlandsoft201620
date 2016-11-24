# - *- coding: utf-8 - *-

from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    val_imagen = models.CharField(max_length=1000, verbose_name='Imágen', help_text='URL de la imágen de usuario',
                                  blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Artista(models.Model):
    """
    Describe un artista.
    """
    nom_artistico = models.CharField(max_length=200)
    nom_pais = models.CharField(max_length=50)
    nom_ciudad = models.CharField(max_length=50)
    val_imagen = models.CharField(max_length=1000, verbose_name='Imágen', help_text='URL de la imagen del artista',
                                  blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    seguidores = models.ManyToManyField(User, related_name='seguidores', blank=True)
    email = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.nom_artistico


class Album(models.Model):
    """
    Describe un album.
    """
    nom_album = models.CharField(max_length=1000, verbose_name='Album', help_text='Nombre del album')
    val_imagen = models.CharField(max_length=1000, verbose_name='Imágen', help_text='URL de la imagen del album',
                                  blank=True)
    fec_creacion_album = models.DateField(auto_now_add=False, help_text='Fecha de creación del album')
    artista = models.ForeignKey(Artista, on_delete=models.CASCADE)

    def __str__(self):
        return self.nom_album


class Audio(models.Model):
    """
    Describe un audio.
    """
    nom_audio = models.CharField(max_length=1000, verbose_name='Audio', help_text='Nombre del audio')
    val_imagen = models.CharField(max_length=1000, verbose_name='Imágen', help_text='URL de la imagen del audio',
                                  blank=True)
    val_recurso = models.CharField(max_length=1000, verbose_name='Recurso', help_text='URL del recurso del audio')
    fec_entrada_audio = models.DateField(auto_now_add=True, help_text='Fecha de subida del audio')
    artistas = models.ManyToManyField(Artista, related_name="artistas")
    likes = models.ManyToManyField(User, related_name="likes", blank=True)
    albums = models.ManyToManyField(Album, related_name="albums", blank=True)
    type_audio = models.CharField(max_length=1000, verbose_name='Audio', help_text='Tipo del audio', blank=True)
    tags_audio = models.CharField(max_length=1000, verbose_name='Audio', help_text='Etiquetas del audio', blank=True)
    ind_estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nom_audio

    def tags_as_list(self):
        return self.tags_audio.split(',')


class Donaciones(models.Model):
    """
    Describe una donación
    """
    valor = models.IntegerField(default=0)
    tarjeta_credito = models.CharField(max_length=200)
    artista = models.ForeignKey(Artista, on_delete=models.CASCADE)
    fec_donacion = models.DateTimeField(auto_now_add=True, help_text='Fecha de donación')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Comentario(models.Model):
    """
    Describe un comentario
    """
    val_comentario = models.TextField()
    fec_creacion_comen = models.DateTimeField(auto_now_add=True, help_text='Fecha de creación del comentario')
    ind_publicado = models.BooleanField(default=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    audio = models.ForeignKey(Audio, on_delete=models.CASCADE)

    def __str__(self):  # __unicode__ on Python 2
        return self.val_comentario

    class Meta:
        ordering = ('val_comentario',)

class Ratings(models.Model):
    """
    Describe una calificación
    """
    val_rating = models.PositiveIntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    fec_creacion_rating = models.DateTimeField(auto_now_add=True, help_text='Fecha de creación del rating')
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    audio = models.ForeignKey(Audio, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('autor', 'audio',)

    def __str__(self):  # __unicode__ on Python 2
        return self.val_rating



class Denuncia(models.Model):
    """
    Describe un video reportado
    """
    val_denuncia = models.TextField(max_length=1000, help_text='denuncia')
    ind_tipo_denuncia = models.CharField(max_length=1000, verbose_name='Tipo denuncia', help_text='Tipo de denuncia')
    fec_creacion_denuncia = models.DateTimeField(auto_now_add=True, help_text='Fecha de creación de la denuncia')
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    audio = models.ForeignKey(Audio, on_delete=models.CASCADE)

    def __str__(self):  # __unicode__ on Python 2
        return self.val_denuncia

    class Meta:
        ordering = ('val_denuncia',)