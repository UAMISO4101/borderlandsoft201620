from django.test import TestCase
from django.test import Client
from contenido.models import Artista


class FollowMeTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        artista = Artista()
        artista.nom_artistico = 'Nombre'
        artista.nom_pais = 'Pais'
        artista.nom_ciudad = 'Ciudad'
        artista.save()

    def follow_me_test(self):
        c = Client()
        response = c.post('/user/1')
        self.assertEqual(response.status_code, 301)
