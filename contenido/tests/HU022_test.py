from django.test import TestCase
from django.test import Client
from contenido.models import Artista
__author__ = 'Luis_Sebastian_Talero'


class HU022_test(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        artista = Artista()
        artista.nom_artistico = 'Luis'
        artista.nom_pais = 'Colombia'
        artista.nom_ciudad = 'Bogota'
        artista.email = 'ls.talero21@uniandes.edu.co'
        artista.save()

    def donation_notification_test(self):
        c = Client()
        response = c.post('/follow/', {'value': 1000, 'credit_card': 12345, 'artist_to_donation': 1})
        self.assertEqual(response.status_code, 200)
