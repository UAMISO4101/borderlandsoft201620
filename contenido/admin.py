from django.contrib import admin
from .models import *


# Register your models here.
class ArtistaAdmin(admin.ModelAdmin):
    list_display = ('nom_artistico', 'nom_pais', 'nom_ciudad')
    search_fields = ('nom_artistico',)


class AudioAdmin(admin.ModelAdmin):
    list_display = ('nom_audio', 'val_imagen', 'val_recurso', 'fec_entrada_audio',)
    search_fields = ('nom_audio',)
    filter_horizontal = ('artistas', 'likes', 'albums')


class AlbumAdmin(admin.ModelAdmin):
    list_display = ('nom_album', 'val_imagen', 'fec_creacion_album', 'artista')
    search_fields = ('nom_album',)


class DonacionesAdmin(admin.ModelAdmin):
    list_display = ('valor', 'tarjeta_credito', 'artista')

admin.site.register(Artista, ArtistaAdmin)
admin.site.register(Audio, AudioAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Donaciones, DonacionesAdmin)

