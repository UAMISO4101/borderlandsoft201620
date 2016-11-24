from django.test import TestCase
from django.urls import reverse
from contenido.models import Audio
from contenido.models import Artista
from contenido.models import Denuncia
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient

MODELS = [Denuncia, Audio, Artista, User]

class DenunciaAPITest(TestCase):
    def setUp(self):
        # Se elimina el contenido de las tablas del modelo
        for model in MODELS:
            if len(model.objects.all()) :
                model.objects.all().delete()

        # Se crea un usuario regular de prueba
        self.usuario_regular = User.objects.create_user(username='William78', email='william78@gmail.com', password='william1234')
        # Se crea un usuario artista
        self.usuario_artista = User.objects.create_user(username='Fanny', email='fanny@gmail.com', password='fanny1234')
        # Se crea un artista al cual se le asociara un audio
        self.artista = Artista.objects.create(nom_artistico='Fanny Lu', nom_pais='Colombia', nom_ciudad='Bogota',
                                              val_imagen='imagen.jpg', user=self.usuario_artista)
        # Se crea un audio para pruebas
        self.audio = Audio.objects.create(nom_audio='La casita de Patylu', val_imagen='imagen4.jpg',
                                          val_recurso='url-recurso.mp3')
        self.audio.artistas.add(self.artista)

        # Se inicializa un cliente de api Rest
        self.client = APIClient()


    # Prueba utilizada para el registro de denuncias mediante el API REST
    def test_comentario_registro(self):
        self.client.login(username='William78', password='william1234')
        url = reverse('denuncia-create')
        data = {'val_denuncia': 'DabApps','ind_tipo_denuncia':'Contenido sexual','autor':self.usuario_regular.id, 'audio':self.audio.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Denuncia.objects.count(), 1)
        self.assertEqual(Denuncia.objects.get().val_denuncia, 'DabApps')