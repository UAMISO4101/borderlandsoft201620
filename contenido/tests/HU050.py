from django.test import TestCase
from django.test import Client
from contenido.models import Artista


class ListaConvocatoriaTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        pass

    def test_lista(self):
        c = Client()
        response = c.post('/convocatoria')
        self.assertEqual(response.status_code, 200)
