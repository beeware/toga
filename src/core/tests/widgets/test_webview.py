import unittest
from unittest.mock import MagicMock, Mock, patch
import toga
import toga_dummy


class TestWebView(unittest.TestCase):
    def setUp(self):
        self.factory = MagicMock()
        self.factory.WebView = MagicMock(return_value=MagicMock(spec=toga_dummy.factory.WebView))

        self.url = 'https://pybee.org/'

        def callback(widget):
            pass

        self.on_key_down = callback
        self.web_view = toga.WebView(url=self.url,
                                     on_key_down=self.on_key_down,
                                     factory=self.factory)

    def test_factory_called(self):
        self.factory.WebView.assert_called_with(interface=self.web_view)

    def test_setting_url_invokes_impl_method(self):
        new_url = 'https://github.com/'
        self.web_view.url = new_url
        self.assertEqual(self.web_view.url, new_url)
        self.web_view._impl.set_url.assert_called_with(new_url)

    def test_set_content_invokes_impl_method(self):
        root_url = 'https://github.com/'
        new_content = '<!DOCTYPE html>' \
                      '<html>' \
                      '<body>' \
                      '<h1>My First Heading</h1>' \
                      '<p>My first paragraph.</p>' \
                      '</body>' \
                      '</html>'

        self.web_view.set_content(root_url, new_content)
        self.web_view._impl.set_content.assert_called_once_with(root_url, new_content)
