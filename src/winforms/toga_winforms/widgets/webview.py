from toga.interface import WebView as WebViewInterface

from .base import WidgetMixin
from ..libs import *


class TogaWebBrowser(WinForms.WebBrowser):
    def __init__(self, interface):
        super().__init__()
        self.interface = interface


class WebView(WebViewInterface, WidgetMixin):
    def __init__(self, id=None, style=None, url=None, user_agent=None, on_key_down=None):
        if user_agent is None:
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240"
        super().__init__(id=id, style=style, url=url, user_agent=user_agent, on_key_down=on_key_down)
        self._create()

    def create(self):
        self._impl = TogaWebBrowser(self)

    def _set_url(self, value):
        if value:
            self._impl.Navigate(Uri(value), "_self", None, "User-Agent: %s" % self.user_agent)

    def _set_content(self, root_url, content):
        self._impl.Navigate(Uri(root_url), "_self" , None, self.user_agent)

    def _set_user_agent(self, value):
        pass

    def evaluate(self, javascript):
        pass
