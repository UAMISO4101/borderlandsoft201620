from django.test import TestCase

from contenido.models import Audio
from contenido.models import Ratings
from contenido.models import Artista
from django.contrib.auth.models import User
from rest_framework.test import APIClient

MODELS = [Ratings, Audio, Artista, User]

class AudioUpdateEstadoAPITest(TestCase):
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


    # Prueba utilizada para la actualización del estado de un audio
    def test_rating_delete(self):
        self.client.login(username='dh.mahecha', password='Ab1234')
        self.client.put('/api/audioestado-update/1', data={'ind_estado' : False})
        self.assertEqual(Audio.objects.count(), 1)
        self.assertEqual(Audio.objects.get().ind_estado, False)


