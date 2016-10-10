from django.contrib import admin
from .models import *

# Register your models here.
class ArtistaAdmin(admin.ModelAdmin):
    list_display = ('nom_artistico', 'nom_pais', 'nom_ciudad')
    search_fields = ('nom_artistico',)

class AudioAdmin(admin.ModelAdmin):
    list_display = ('nom_audio', 'val_imagen', 'val_recurso', 'fec_entrada_audio',)
    search_fields = ('nom_audio',)
    filter_horizontal = ('artistas','likes','albums')

class AlbumAdmin(admin.ModelAdmin):
    list_display = ('val_imagen', 'nom_album','fec_creacion_album','artista')
    search_fields = ('nom_album',)




admin.site.register(Artista, ArtistaAdmin)
admin.site.register(Audio, AudioAdmin)
admin.site.register(Album, AlbumAdmin)

