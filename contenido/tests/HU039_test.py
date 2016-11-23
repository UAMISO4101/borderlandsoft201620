# - *- coding: utf-8 - *-

from unittest import TestCase
from selenium import webdriver
from contenido.tests.util import Util


class HU039Test(TestCase):
    def setUp(self):
        self._util = Util(site=self)
        self._username = 'lindsey'
        self._password = 'qqwwqqwwq'
        self.browser = webdriver.Firefox()
        self.browser.get('http://localhost:8000/accounts/login')

    # def tearDown(self):

    def login(self):
        self._util.set_text('txtUser', self._username)
        self._util.set_text('txtPassword', self._password)
        self._util.set_click('btnLogin')
        self.browser.get('http://localhost:8000/song/5/')

    def abrir_modal_agregar_audio_a_album(self):
        self.login()
        self._util.set_click('addToAlbumButton')
        self.browser.implicitly_wait(2)
        self.assertIn(self._util.get_class_attr("addToAlbumModal"), "modal fade in")

    def abrir_y_cerrar_modal_agregar_audio_a_album(self):
        self.abrir_modal_agregar_audio_a_album()
        self.browser.implicitly_wait(2)
        self._util.set_click('btnCloseAddToAlbumModal')
        self.assertIn("modal fade", self._util.get_class_attr("addToAlbumModal"))
