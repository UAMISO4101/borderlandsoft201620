from django.test import TestCase
from django.test import Client
from contenido.models import Artista


# Create your tests here.


class SendNotificationFollowTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        artista = Artista()
        artista.nom_artistico = 'Nombre'
        artista.nom_pais = 'Pais'
        artista.nom_ciudad = 'Ciudad'
        artista.save()

    def follow_notification_test(self):
        artista = Artista.objects.get(pk=1)
        total_follow_before = artista.seguidores.count()
        c = Client()
        response = c.post('/follow/', {'artist_id': 1})
        artista = Artista.objects.get(pk=1)
        total_follow_after = artista.seguidores.count()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(total_follow_after, total_follow_before)
        artista.save()
