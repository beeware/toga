from travertino.size import at_least

from ..keys import toga_key
from ..libs import WebKit2
from .base import Widget


class WebView(Widget):
    """ GTK WebView implementation.

    """
    def create(self):
        if WebKit2 is None:
            raise RuntimeError(
                "Import 'from gi.repository import WebKit' failed;" +
                " may need to install gir1.2-webkit2-4.0 or gir1.2-webkit2-3.0.")

        self.native = WebKit2.WebView()
        self.native.interface = self.interface

        self.native.connect('key-press-event', self.gtk_on_key)
        self._last_key_time = 0

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
            self.native.load_uri(self.interface.url)

    def set_user_agent(self, value):
        # replace user agent of webview (webview has own one)
        self.native.get_settings().props.user_agent = value

    def set_content(self, root_url, content):
        self.native.load_html(content, root_url)

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
        self.native.run_javascript(javascript, None, gtk_js_finished)

        # wait for the future, and return the result
        await future
        return future.result()

    def invoke_javascript(self, javascript):
        # Invoke the javascript without a callback.
        self.native.run_javascript(javascript, None, None)

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface.MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface.MIN_HEIGHT)
