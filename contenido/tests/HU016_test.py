from django.test import TestCase
from django.test import Client
from contenido.models import Audio


# Create your tests here.


class AudioUploadTests(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        pass

    def upload_audio_test_view(self):
        c = Client()
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
