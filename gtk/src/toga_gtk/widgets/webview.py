from travertino.size import at_least

from toga.widgets.webview import JavaScriptResult

from ..libs import WebKit2
from .base import Widget


class WebView(Widget):
    """GTK WebView implementation."""

    def create(self):
        if WebKit2 is None:
            raise RuntimeError(
                "Unable to import WebKit2. Ensure that the system package "
                "providing Webkit2 and its GTK bindings have been installed."
            )

        self.native = WebKit2.WebView()

        settings = self.native.get_settings()
        settings.set_property("enable-developer-extras", True)

        # The default cache model is WEB_BROWSER, which will
        # use the backing cache to minimize hits on the web server.
        # This can result in stale web content being served, even if
        # the source document (and the web server response) changes.
        context = self.native.get_context()
        context.set_cache_model(WebKit2.CacheModel.DOCUMENT_VIEWER)

        self.native.connect("load-changed", self.gtk_on_load_changed)

    def gtk_on_load_changed(self, widget, load_event, *args):
        if load_event == WebKit2.LoadEvent.FINISHED:
            if self.interface.on_webview_load:
                self.interface.on_webview_load(self.interface)

    def get_url(self):
        return self.native.get_uri()

    def set_url(self, value, future=None):
        if value:
            self.native.load_uri(value)

    def set_user_agent(self, value):
        # replace user agent of webview (webview has own one)
        self.native.get_settings().props.user_agent = value

    def set_content(self, root_url, content):
        self.native.load_html(content, root_url)

    def evaluate_javascript(self, javascript, on_result=None):
        # Construct a future on the event loop
        result = JavaScriptResult()

        # Define a callback that will update the future when
        # the Javascript is complete.
        def gtk_js_finished(webview, task, *user_data):
            """If `run_javascript_finish` from GTK returns a result, unmarshal it, and
            call back with the result."""
            result = webview.run_javascript_finish(task)
            if result:
                result = result.get_js_value().to_string()
            result.future.set_result(result)

        # Invoke the javascript method, with a callback that will set
        # the future when a result is available.
        self.native.run_javascript(javascript, None, gtk_js_finished)

        # wait for the future, and return the result
        return result

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface._MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface._MIN_HEIGHT)
