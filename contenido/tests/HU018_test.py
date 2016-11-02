# - *- coding: utf-8 - *-

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

    def ingresar_album(self, name, file):
        script = "document.getElementById('inputFileAlbumImg').style.display = "
        self.abrir_modal_agregar_album()
        self.browser.implicitly_wait(2)
        self.browser.execute_script(script + "'block';")
        self._util.set_text('inputFileAlbumImg', file)
        self.browser.execute_script(script + "'none';")
        self._util.set_text('txtNombreAlbum', name)
        self.browser.find_element_by_xpath("//select[@name='upload_album_year']/option[text()='2016']").click()
        self._util.set_click('btnSaveAlbum')
        self.browser.implicitly_wait(2)

    def ingresar_album_sin_nombre(self):
        self.ingresar_album('', 'C:\img.png')
        self.assertIn("form-group has-error", self._util.get_class_attr("formGroupNombreAlbum"))

    def ingresar_imagen_otra_extension(self):
        self.ingresar_album('Los 3 sprints bailables', 'C:\img.txt')
        self.assertIn("form-group input-group has-error", self._util.get_class_attr("formGroupAlbumImg"))

    def ingresar_album_formulario_completo(self):
        self.ingresar_album('Los 3 sprints bailables', 'C:\img.png')
        self.assertIn("/album/", self.browser.current_url)
