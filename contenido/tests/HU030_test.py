from django.test import TestCase
from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User



# Create your tests here.


class ActualizarInfoTest(TestCase):
    def setUp(self):
        # Se crea un usuario regular de prueba
        self.usuario_regular = User.objects.create_user(username='William78', email='william78@gmail.com',
                                                        password='william1234')



    def test_update_user(self):
        self.client.login(username='William78', password='william1234')

        c = Client()
        response = c.post(reverse('editar_informacion', kwargs={'pk': self.usuario_regular.id}),
                          {'first_name': 'UsuarioPrueba', 'last_name': 'LastName',
                            'upload_user_img': '',})
        usuario = User.objects.get(pk=1)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(usuario.first_name, 'UsuarioPrueba')
