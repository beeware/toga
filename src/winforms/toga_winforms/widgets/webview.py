from toga.interface import WebView as WebViewInterface

from .base import WidgetMixin
from ..libs import *


class TogaWebBrowser(WinForms.WebBrowser):
    def __init__(self, interface):
        super().__init__()
        self.interface = interface


class WebView(WebViewInterface, WidgetMixin):
    def __init__(self, id=None, style=None, url=None, on_key_down=None):
        super().__init__(id=id, style=style, url=url, on_key_down=on_key_down)
        self._create()

    def create(self):
        self._impl = TogaWebBrowser(self)

    def _set_url(self, value):
        if value:
            self._impl.Navigate(Uri(value))

    def _set_content(self, root_url, content):
        # self._impl.mainFrame.loadHTMLString_baseURL_(content, NSURL.URLWithString_(root_url))
        self._impl.Navigate(Uri(root_url))

    def evaluate(self, javascript):
        # return self._impl.stringByEvaluatingJavaScriptFromString_(javascript)
        pass
