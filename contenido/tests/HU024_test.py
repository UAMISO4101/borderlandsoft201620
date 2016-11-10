from django.test import TestCase
from django.test import Client
from contenido.models import Audio


# Create your tests here.


class SendNotificationLikeTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        audio = Audio()
        audio.nom_audio = "song1"
        audio.val_recurso = "http://la...."
        audio.fec_entrada_audio = "2016-10-08"
        audio.save()

    def like_notification_test(self):
        audio = Audio.objects.get(pk=1)
        total_likes_before = audio.likes.count()
        c = Client()
        response = c.post('/like/', {'song_id': 1})
        audio = Audio.objects.get(pk=1)
        total_likes_after = audio.likes.count()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(total_likes_after, total_likes_before)
