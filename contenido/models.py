from __future__ import unicode_literals
from django.db import models

class Artista(models.Model):
    """
    Describe un artista.
    """
    nom_artistico = models.CharField(max_length=200)
    nom_pais = models.CharField(max_length=50)
    nom_ciudad = models.CharField(max_length=50)

    def __str__(self):
        return self.nom_artistico

class Audio(models.Model):
    """
    Describe un audio.
    """
    nom_audio = models.CharField(max_length=1000, verbose_name='Audio', help_text='Nombre del audio')
    val_imagen = models.CharField(max_length=1000, verbose_name='Imágen', help_text='URL de la imagen del audio', blank=True)
    val_recurso = models.CharField(max_length=1000, verbose_name='Recurso', help_text='URL del recurso del audio')
    fec_entrada_audio = models.DateField(auto_now=True, help_text='Fecha de subida del audio')
    artista = models.ForeignKey(Artista, on_delete=models.CASCADE)

    def __str__(self):
        return self.nom_audio

class Album(models.Model):
    """
    Describe un album.
    """
    val_imagen = models.CharField(max_length=1000, verbose_name='Imágen', help_text='URL de la imagen del album', blank=True)
    nom_album = models.CharField(max_length=1000, verbose_name='Album', help_text='Nombre del album')
    fec_creacion_album = models.DateField(auto_now=True,help_text='Fecha de creación del album')

    def __str__(self):
        return self.nom_album


class Artista_album(models.Model):
    """
    Describe la relación entre artista y album
    """
    artista = models.ForeignKey(Artista, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)

class Album_audio(models.Model):
    """
    Describe la relación entre album y audio
    """
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    audio = models.ForeignKey(Audio, on_delete=models.CASCADE)
    fec_asociacion_audio = models.DateField(auto_now=True, help_text='Fecha de asociación de audio a album')