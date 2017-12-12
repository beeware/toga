from toga_winforms.libs import *

from .base import Widget


class TogaWebBrowser(WinForms.WebBrowser):
    def __init__(self, interface):
        super().__init__()
        self.interface = interface


class WebView(Widget):
    def create(self):
        self.native = TogaWebBrowser(self)

    def set_url(self, value):
        if value:
            self.native.Navigate(Uri(value), "_self", None, "User-Agent: %s" % self.interface.user_agent)

    def set_content(self, root_url, content):
        self.native.Navigate(Uri(root_url), "_self" , None, self.interface.user_agent)

    def get_dom(self):
        raise NotImplementedError()

    def set_user_agent(self, value):
        self.native.customUserAgent = value if value else "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240"

    def evaluate(self, javascript):
        raise NotImplementedError()

