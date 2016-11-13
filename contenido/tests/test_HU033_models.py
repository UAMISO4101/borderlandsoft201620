from django.test import TestCase

from contenido.models import Audio, Ratings, Artista
from django.contrib.auth.models import User

MODELS = [Ratings, Audio, Artista, User]

class AudioUpdateEstadoTest(TestCase):
    def setUp(self):
        # Se elimina el contenido de las tablas del modelo
        for model in MODELS:
            if len(model.objects.all()):
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


    # Prueba utilizada la eliminación de ratings mediante acceso a datos directo
    def test_update_estado(self):
        instance = Audio.objects.filter(id=self.audio.id).update(ind_estado=False)
        audioTest = Audio.objects.filter(id=self.audio.id)
        self.assertEqual(audioTest[0].ind_estado, False)