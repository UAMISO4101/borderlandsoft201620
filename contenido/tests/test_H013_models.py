from django.test import TestCase

from contenido.models import Audio
from contenido.models import Comentario
from contenido.models import Artista
from django.contrib.auth.models import User

MODELS = [Comentario, Audio, Artista, User]


class ComentarioTest(TestCase):
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

    # Prueba utilizada para el registro de comentarios mediante acceso a datos directo
    def test_comentario_registro(self):
        instance = Comentario.objects.create(val_comentario='Una estupenda cancion', autor=self.usuario_regular, audio=self.audio)
        self.assertEqual(instance.__str__(), "Una estupenda cancion")


    # Prueba utilizada para la consulta de comentarios
    def test_comentario_consultar(self):
        Comentario.objects.create(val_comentario='Una estupenda cancion 1',autor=self.usuario_regular,audio=self.audio)
        Comentario.objects.create(val_comentario='Una estupenda cancion 2',autor=self.usuario_regular,audio=self.audio)

        comentarios = Comentario.objects.all()

        self.assertEqual(len(comentarios), 2)
