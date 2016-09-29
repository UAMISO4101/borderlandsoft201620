from django.contrib import admin
from .models import *

# Register your models here.
class ArtistaAdmin(admin.ModelAdmin):
    list_display = ('nom_artistico', 'nom_pais', 'nom_ciudad')
    search_fields = ('nom_artistico',)

class AudioAdmin(admin.ModelAdmin):
    list_display = ('nom_audio', 'val_imagen', 'val_recurso', 'artista')
    search_fields = ('nom_audio',)

admin.site.register(Artista, ArtistaAdmin)
admin.site.register(Audio, AudioAdmin)
