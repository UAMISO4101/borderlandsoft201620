from unittest import TestCase
from selenium import webdriver
from contenido.tests.util import Util


class HU018Test(TestCase):
    def setUp(self):
        self._util = Util(site=self)
        self._username = 'hollens'
        self._password = 'qqwwqqwwq'
        self.browser = webdriver.Firefox()
        self.browser.get('http://localhost:8000/accounts/login')

    # def tearDown(self):

    def login(self):
        self._util.set_text('txtUser', self._username)
        self._util.set_text('txtPassword', self._password)
        self._util.set_click('btnLogin')

    def abrir_modal_agregar_album(self):
        self.login()
        self._util.set_click('addObjectMenu')
        self._util.set_click('addNewAlbumBtn')
        self.browser.implicitly_wait(2)
        self.assertIn(self._util.get_class_attr("newAlbum"), "modal fade in")

    def abrir_y_cerrar_modal_agregar_album(self):
        self.abrir_modal_agregar_album()
        self.browser.implicitly_wait(2)
        self._util.set_click('btnCloseAlbumModal')
        self.assertIn("modal fade", self._util.get_class_attr("newAlbum"))
