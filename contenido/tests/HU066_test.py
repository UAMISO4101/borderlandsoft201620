from django.test import TestCase
from django.test import Client

from contenido.models import Audio
from contenido.models import Artista
from django.contrib.auth.models import User



# Create your tests here.


class AudioUploadWithUserTests(TestCase):
    def setUp(self):
        # Se crea un usuario regular de prueba
        self.usuario_regular = User.objects.create_user(username='William78', email='william78@gmail.com',
                                                        password='william1234')
        # Se crea un usuario artista
        self.usuario_artista = User.objects.create_user(username='jdelafonte', email='jdelafonte@gmail.com',
                                                        password='JFonte1234')
        # Se crea un artista al cual se le asociara un audio
        self.artista = Artista.objects.create(nom_artistico='Javier de la Fonte', nom_pais='Colombia',
                                              nom_ciudad='Bogota',
                                              val_imagen='imagen.jpg', user=self.usuario_artista)

    def test_upload_audio_with_artista(self):
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


    def test_upload_audio_with_user(self):
        c = Client()
        c.login(username='William78', password='william1234')

        with open('SonidosLibres/fixtures/init.json') as song_file:
            with open('SonidosLibres/fixtures/init.json') as image_file:
                song_name = 'TestSongName'
                response = c.post('/upload/song/',
                                  {'upload_song_name': song_name, 'upload_song_type': 'Rock',
                                   'upload_song_tags': 'Tag1',
                                   'upload_song_file_file': song_file, 'upload_song_img_file': image_file,
                                   'upload_nombre_artistico': 'Fonte Marc', 'upload_pais_origen': 'Colombia',
                                    'upload_ciudad_origen': 'Bogota',})
        audio = Audio.objects.get(pk=1)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(audio.nom_audio, song_name)
