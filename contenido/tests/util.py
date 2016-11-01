class Util:
    def __init__(self, site):
        self._site = site

    def set_text(self, key, string):
        nombre = self._site.browser.find_element_by_id(key)
        nombre.clear()
        nombre.send_keys(string)

    def set_click(self, key):
        link = self._site.browser.find_element_by_id(key)
        link.click()

    def assert_text(self, xpath, expected):
        html = self._site.browser.find_element_by_xpath(xpath)
        self._site.assertIn(expected, html.text)