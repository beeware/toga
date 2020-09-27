from travertino.size import at_least

from toga_winforms.libs import Uri, WinForms

from .base import Widget


class TogaWebBrowser(WinForms.WebBrowser):
    def __init__(self, interface):
        super().__init__()
        self.interface = interface


class WebView(Widget):
    def create(self):
        self.native = TogaWebBrowser(self)

    def set_on_key_down(self, handler):
        pass

    def set_on_webview_load(self, handler):
        pass

    def set_url(self, value):
        if value:
            self.native.Navigate(Uri(self.interface.url), "_self", None, "User-Agent: %s" % self.interface.user_agent)

    def set_content(self, root_url, content):
        self.native.Url = Uri(root_url)
        self.native.DocumentText = content

    def get_dom(self):
        self.interface.factory.not_implemented('WebView.get_dom()')

    def set_user_agent(self, value):
        user_agent = value if value else "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240"  # NOQA
        self.native.customUserAgent = user_agent

    async def evaluate_javascript(self, javascript):
        self.interface.factory.not_implemented('WebView.evaluate_javascript()')

    def invoke_javascript(self, javascript):
        self.interface.factory.not_implemented('WebView.invoke_javascript()')

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface.MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface.MIN_HEIGHT)
