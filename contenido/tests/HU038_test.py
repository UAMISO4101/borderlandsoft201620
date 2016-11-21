from django.test import TestCase
from django.test import Client
from contenido.models import Artista


class DeleteAlbumTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        artista = Artista()
        artista.nom_artistico = 'Nombre'
        artista.nom_pais = 'Pais'
        artista.nom_ciudad = 'Ciudad'
        artista.save()
        album = Album()
        album.nom_album = 'prueba'
        album.fec_creacion_album = datetime.datetime( )
        album.artista = artista
        album.save()


    def test_delete(self):
        c = Client()
        response = c.post('/album/1/delete')
        self.assertEqual(response.status_code, 301)
