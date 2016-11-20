from django.test import TestCase
from django.urls import reverse
from datetime import datetime

from contenido.models import Audio
from contenido.models import Comentario
from contenido.models import Artista
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient

MODELS = [Comentario, Audio, Artista, User]

class ComentarioAPITest(TestCase):
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

    # Prueba utilizada para el registro de comentarios mediante el API REST
    def test_comentario_registro(self):
        self.client.login(username='William78', password='william1234')
        url = reverse('comment-create')
        data = {'val_comentario': 'DabApps','ind_publicado':True,'autor':self.usuario_regular.id, 'audio':self.audio.id, 'fec_creacion_comen':datetime.now()}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comentario.objects.count(), 1)
        self.assertEqual(Comentario.objects.get().val_comentario, 'DabApps')

    # Prueba utilizada para la consulta de comentarios mediante el API REST
    def test_comentario_consultar(self):
        self.client.login(username='William78', password='william1234')
        url = reverse('comment-create')
        data = {'val_comentario': 'DabApps', 'ind_publicado': True, 'autor': self.usuario_regular.id,
                'audio': self.audio.id, 'fec_creacion_comen':datetime.now()}
        response = self.client.post(url, data, format='json')

        url =  reverse('coments_list', kwargs={'song_id':4})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Comentario.objects.count(), 1)
        self.assertEqual(Comentario.objects.get().val_comentario, 'DabApps')

