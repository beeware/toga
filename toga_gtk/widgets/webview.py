from __future__ import print_function, absolute_import, division

from gi.repository import Gtk

# The following import will fail if WebKit or it's API wrappers aren't
# installed; handle failure gracefully
# (see https://github.com/pybee/toga/issues/26)
try:
    from gi.repository import WebKit
except ImportError:
    WebKit = None

from .base import Widget


class WebView(Widget):
    def __init__(self, url=None):
        super(WebView, self).__init__()

        self.startup()

        self.url = url

    def startup(self):
        if WebKit is None:
            raise RuntimeError(
                "Import 'from gi.repository import WebKit' failed;" +
                " may need to install gir1.2-webkit-3.0 or similar.")

        self._impl = Gtk.ScrolledWindow()
        self._impl.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)

        self._webview = WebKit.WebView()

        self._impl.add(self._webview)
        self._impl.set_min_content_width(200)
        self._impl.set_min_content_height(200)

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value
        if self._url:
            self._webview.load_uri(self._url)
