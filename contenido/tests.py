from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from contenido.models import Audio


# Create your tests here.


class ContenidoTests(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        user = User.objects.create_user(
            username='userTest', email='userTest@com.co', password='Seneca2016')
        audio = Audio()
        audio.nom_audio = "song1"
        audio.val_recurso = "http://la...."
        audio.fec_entrada_audio = "2016-10-08"
        audio.save()
        audio.likes.add(User.objects.get(id=user.id))
        audio.save()

    def unlike_test_view(self):
        audio = Audio.objects.get(pk=1)
        total_likes_before = audio.likes.count()
        c = Client()
        response = c.post('/unlike/', {'song_id': 1})
        audio = Audio.objects.get(pk=1)
        audio.likes.remove(User.objects.get(id=1))
        total_likes_after = audio.likes.count()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(total_likes_after, total_likes_before - 1)
