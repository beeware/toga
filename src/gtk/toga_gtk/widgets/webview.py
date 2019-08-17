import time

from toga_gtk.libs import Gtk, WebKit2, Gdk

from .base import Widget
from ..keys import gdk_key


class WebView(Widget):
    """ GTK WebView implementation.

    TODO: WebView is not displaying anything when setting a url.
    """

    def create(self):
        if WebKit2 is None:
            raise RuntimeError(
                "Import 'from gi.repository import WebKit' failed;" +
                " may need to install gir1.2-webkit2-4.0 or gir1.2-webkit2-3.0.")

        self.native = Gtk.ScrolledWindow()
        self.native.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.native.interface = self.interface

        self.webview = WebKit2.WebView()

        self.native.add(self.webview)
        self.native.set_min_content_width(200)
        self.native.set_min_content_height(200)

        self.webview.connect('key-press-event', self.on_key)
        self._last_key_time = 0

        # self.native.connect('show', lambda event: self.rehint())

    def on_key(self, widget, event, *args):
        if event.time > self._last_key_time and self.interface.on_key_down:
            self._last_key_time = event.time
            toga_event = gdk_key(event)
            if toga_event:
                self.interface.on_key_down(**toga_event)

    def set_url(self, value):
        if value:
            self.webview.load_uri(self.interface.url)

    def set_user_agent(self, value):
        self.interface.factory.not_implemented('Window.info_dialog()')
        # self.native.user_agent = value if value else "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36"

    def set_content(self, root_url, content):
        self.webview.load_html(content, root_url)

    def get_dom(self):
        self.interface.factory.not_implemented('WebView.get_dom()')

    def evaluate(self, javascript, callback):

        def _cb(webview, task, *user_data):
            finish = self.webview.run_javascript_finish(task)
            print(finish)
            if finish:
                finish = finish.get_js_value().to_string()
            print(finish)
            callback(finish)

        if callback:
            self.webview.run_javascript(javascript, None, _cb)
        else:
            self.webview.run_javascript(javascript, None, None)
