import gi
from gi.repository import Gtk

# The following import will fail if WebKit or it's API wrappers aren't
# installed; handle failure gracefully
# (see https://github.com/pybee/toga/issues/26)
try:
    gi.require_version('WebKit2', '3.0')
    from gi.repository import WebKit2
except ImportError:
    WebKit2 = None

from toga.interface import WebView as WebViewInterface

from .base import WidgetMixin


class WebView(WebViewInterface, WidgetMixin):
    def __init__(self, id=None, style=None, url=None, on_key_down=None):
        super().__init__(id=id, style=style, url=url, on_key_down=on_key_down)
        self._create()

    def create(self):
        if WebKit2 is None:
            raise RuntimeError(
                "Import 'from gi.repository import WebKit' failed;" +
                " may need to install gir1.2-webkit-3.0 or similar.")

        self._impl = Gtk.ScrolledWindow()
        self._impl.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self._impl._interface = self

        self._webview = WebKit2.WebView()

        self._impl.add(self._webview)
        self._impl.set_min_content_width(200)
        self._impl.set_min_content_height(200)

        self._impl.connect('show', lambda event: self.rehint())

    def _set_url(self, value):
        if value:
            self._webview.load_uri(self._url)

    def _set_content(self, root_url, content):
        # self._impl.mainFrame.loadHTMLString_baseURL_(content, NSURL.URLWithString_(root_url))
        pass

    def evaluate(self, javascript):
        # FIXME - work out how to run javascript in a webkit view.
        return False
        return self._impl.stringByEvaluatingJavaScriptFromString_(javascript)
