from django.test import TestCase
from django.test import Client

from contenido.models import Audio
from contenido.models import Artista
from django.contrib.auth.models import User


# Create your tests here.


class AudioUploadTests(TestCase):
    def setUp(self):
        # Se crea un usuario artista
        self.usuario_artista = User.objects.create_user(username='jdelafonte', email='jdelafonte@gmail.com',
                                                        password='JFonte1234')
        # Se crea un artista al cual se le asociara un audio
        self.artista = Artista.objects.create(nom_artistico='Javier de la Fonte', nom_pais='Colombia',
                                              nom_ciudad='Bogota',
                                              val_imagen='imagen.jpg', user=self.usuario_artista)

    def upload_audio_test_view(self):
        c = Client()
        c.login(username='jdelafonte', password='JFonte1234')
        with open('SonidosLibres/fixtures/init.json') as song_file:
            with open('SonidosLibres/fixtures/init.json') as image_file:
                song_name = 'TestSongName'
                response = c.post('/upload/song/',
                                  {'upload_song_name': song_name, 'upload_song_type': 'Rock',
                                   'upload_song_tags': 'Tag1',
                                   'upload_song_file_file': song_file, 'upload_song_img_file': image_file})
        audio = Audio.objects.get(pk=1)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(audio.nom_audio, song_name)
