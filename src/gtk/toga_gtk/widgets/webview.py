from ..keys import toga_key
from ..libs import Gtk, WebKit2
from .base import Widget


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

        self.webview.connect('key-press-event', self.gtk_on_key)
        self._last_key_time = 0

        # self.native.connect('show', lambda event: self.rehint())

    def set_on_key_down(self, handler):
        pass

    def set_on_webview_load(self, handler):
        pass

    def gtk_on_key(self, widget, event, *args):
        # key-press-event on WebKit on GTK double-sends events, but they have
        # the same time key. Check for it before we register the press.
        if event.time > self._last_key_time and self.interface.on_key_down:
            self._last_key_time = event.time
            toga_event = toga_key(event)
            if toga_event:
                self.interface.on_key_down(self.interface, **toga_event)

    def set_url(self, value):
        if value:
            self.webview.load_uri(self.interface.url)

    def set_user_agent(self, value):
        self.interface.factory.not_implemented('Window.info_dialog()')
        # user_agent = value if value else "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36"  # NOQA
        # self.native.user_agent = user_agent

    def set_content(self, root_url, content):
        self.webview.load_html(content, root_url)

    def get_dom(self):
        self.interface.factory.not_implemented('WebView.get_dom()')

    async def evaluate_javascript(self, javascript):
        # Construct a future on the event loop
        future = self.interface.window.app._impl.loop.create_future()

        # Define a callback that will update the future when
        # the Javascript is complete.
        def gtk_js_finished(webview, task, *user_data):
            """
            If `run_javascript_finish` from GTK returns a result, unmarshal it,
            and call back with the result.
            """
            result = webview.run_javascript_finish(task)
            if result:
                result = result.get_js_value().to_string()
            future.set_result(result)

        # Invoke the javascript method, with a callback that will set
        # the future when a result is available.
        self.webview.run_javascript(javascript, None, gtk_js_finished)

        # wait for the future, and return the result
        await future
        return future.result()

    def invoke_javascript(self, javascript):
        # Invoke the javascript without a callback.
        self.webview.run_javascript(javascript, None, None)
