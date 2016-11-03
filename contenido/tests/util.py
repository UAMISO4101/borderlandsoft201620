# - *- coding: utf-8 - *-

class Util:
    def __init__(self, site):
        self._site = site

    def set_text(self, key, string):
        obj = self._site.browser.find_element_by_id(key)
        obj.clear()
        obj.send_keys(string)

    def get_class_attr(self, key):
        obj = self._site.browser.find_element_by_id(key)
        return obj.get_attribute('class')

    def set_click(self, key):
        link = self._site.browser.find_element_by_id(key)
        link.click()

    def assert_text(self, xpath, expected):
        html = self._site.browser.find_element_by_xpath(xpath)
        self._site.assertIn(expected, html.text)