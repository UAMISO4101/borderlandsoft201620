from django.test import TestCase

from contenido.models import Audio, Artista, Album
from django.contrib.auth.models import User

MODELS = [Audio, Artista, User, Album]

class InfoContenidoTest(TestCase):
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

        # Se crea un audio para pruebas
        self.audio = Audio.objects.create(nom_audio='Que pecado Existe?', val_imagen='imagen4.jpg',
                                          val_recurso='url-recurso.mp3')


    # Prueba utilizada para la consulta de artistas
    def test_artista_consultar(self):
        # Se crea un artista al cual se le asociara un audio
        self.artista = Artista.objects.create(nom_artistico='Javier de la Fonte', nom_pais='Colombia', nom_ciudad='Bogota',
                                              val_imagen='imagen.jpg', user=self.usuario_artista)

        self.audio.artistas.add(self.artista)
        artistas = Artista.objects.all()
        self.assertEqual(len(artistas), 1)


    def test_album_consultar(self):
        # Se crea un artista al cual se le asociara un audio
        self.artista = Artista.objects.create(nom_artistico='Javier de la Fonte', nom_pais='Colombia', nom_ciudad='Bogota',
                                              val_imagen='imagen.jpg', user=self.usuario_artista)

        self.album = Album.objects.create(nom_album='La Crema', val_imagen='imagenAlbum.jpg', fec_creacion_album='2016-10-31', artista_id=self.artista.id)

        self.audio.albums.add(self.album)
        albums = Album.objects.all()
        self.assertEqual(len(albums), 1)