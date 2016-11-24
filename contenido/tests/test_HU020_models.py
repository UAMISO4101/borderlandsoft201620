from django.test import TestCase

from contenido.models import Audio, Artista, Donaciones
from django.contrib.auth.models import User

MODELS = [Audio, Artista, User, Donaciones]

# Test de Consulta de donaciones
class ConsultaDonacionesTest(TestCase):
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


        # Se crea un artista al cual se le asociara la donación
        self.artista = Artista.objects.create(nom_artistico='Javier de la Fonte', nom_pais='Colombia', nom_ciudad='Bogota',
                                              val_imagen='imagen.jpg', user=self.usuario_artista)

        self.donacion = Donaciones.objects.create(valor=50000, tarjeta_credito = '1111111', artista_id=self.artista.id, fec_donacion='2016-11-19', user_id=self.usuario_regular.id)



    # Prueba utilizada para la consulta de donaciones
    def test_consultar_donacion(self):
        donaciones = Donaciones.objects.all()
        self.assertEqual(len(donaciones), 1)