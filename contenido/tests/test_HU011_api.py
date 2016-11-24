from django.test import TestCase
from django.urls import reverse


from contenido.models import Audio
from contenido.models import Ratings
from contenido.models import Artista
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient

MODELS = [Ratings, Audio, Artista, User]

class RatingsAPITest(TestCase):
    def setUp(self):
        # Se elimina el contenido de las tablas del modelo
        for model in MODELS:
            if len(model.objects.all()) :
                model.objects.all().delete()

        # Se crea un usuario regular de prueba
        self.usuario_regular = User.objects.create_user(username='dh.mahecha', email='dh.mahecha@uniandes.edu.co',
                                                        password='Ab1234')
        # Se crea un usuario artista
        self.usuario_artista = User.objects.create_user(username='jdelafonte', email='jdelafonte@gmail.com', password='JFonte1234')
        # Se crea un artista al cual se le asociara un audio
        self.artista = Artista.objects.create(nom_artistico='Javier de la Fonte', nom_pais='Colombia', nom_ciudad='Bogota',
                                              val_imagen='imagen.jpg', user=self.usuario_artista)
        # Se crea un audio para pruebas
        self.audio = Audio.objects.create(nom_audio='Que pecado Existe?', val_imagen='imagen4.jpg',
                                          val_recurso='url-recurso.mp3')
        self.audio.artistas.add(self.artista)

        # Se inicializa un cliente de api Rest
        self.client = APIClient()


    # Prueba utilizada para el registro de ratings mediante el API REST
    def test_rating_registro(self):
        self.client.login(username='dh.mahecha', password='Ab1234')
        url = reverse('rating-create')
        data = {'val_rating': 5,'autor':self.usuario_regular.id, 'audio':self.audio.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ratings.objects.count(), 1)
        self.assertEqual(Ratings.objects.get().val_rating, 5)