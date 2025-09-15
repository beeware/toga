from http.cookiejar import CookieJar

from travertino.size import at_least

from toga.widgets.webview import CookiesResult, JavaScriptResult

from ..libs import GTK_VERSION, GLib, WebKit2
from .base import Widget


class WebView(Widget):
    """GTK WebView implementation."""

    def create(self):
        if GTK_VERSION >= (4, 0, 0):  # pragma: no-cover-if-gtk3
            raise RuntimeError("WebView isn't supported on GTK4 (yet!)")

        if WebKit2 is None:  # pragma: no cover
            raise RuntimeError(
                "Unable to import WebKit2. Ensure that the system package providing "
                "WebKit2 and its GTK bindings have been installed. See "
                "https://toga.readthedocs.io/en/stable/reference/api/widgets/mapview.html#system-requirements "  # noqa: E501
                "for details."
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

        self.load_future = None

    def gtk_on_load_changed(self, widget, load_event, *args):
        if load_event == WebKit2.LoadEvent.FINISHED:
            self.interface.on_webview_load()

            if self.load_future:
                self.load_future.set_result(None)
                self.load_future = None

    def get_url(self):
        url = self.native.get_uri()
        return None if url == "about:blank" else url

    def _loaded(self, data):
        # Internal method to fake a load event.
        self.native.emit("load-changed", WebKit2.LoadEvent.FINISHED)
        return False

    def set_url(self, value, future=None):
        if value:
            self.native.load_uri(value)
        else:
            self.native.load_plain_text("")
            # GTK doesn't emit a load-changed signal when plain text is loaded; so we
            # fake it. We can't emit the signal directly because it will be handled
            # immediately. During creation of an empty webview, the URL is set to None,
            # which means an event can be triggered before the widget instance has
            # finished construction. So, we defer the call with a 0 timeout.
            GLib.timeout_add(0, self._loaded, None)

        self.load_future = future

    def get_user_agent(self):
        return self.native.get_settings().props.user_agent

    def set_user_agent(self, value):
        # replace user agent of webview (webview has own one)
        self.native.get_settings().props.user_agent = value

    def set_content(self, root_url, content):
        self.native.load_html(content, root_url)

    def get_cookies(self):
        # Create the result object
        result = CookiesResult()
        result.set_result(CookieJar())

        # Signal that this feature is not implemented on the current platform
        self.interface.factory.not_implemented("webview.cookies")

        return result

    def evaluate_javascript(self, javascript, on_result=None):
        # Construct a future on the event loop
        result = JavaScriptResult(on_result)

        # Define a callback that will update the future when
        # the Javascript is complete.
        def gtk_js_finished(webview, task, *user_data):
            """If `evaluate_javascript_finish` from GTK returns a result, unmarshal it,
            and call back with the result."""
            try:
                value = webview.evaluate_javascript_finish(task)
                if value.is_boolean():
                    value = value.to_boolean()
                elif value.is_number():
                    value = value.to_double()
                else:
                    value = value.to_string()

                result.set_result(value)
            except Exception as e:
                exc = RuntimeError(str(e))
                result.set_exception(exc)

        # Invoke the javascript method, with a callback that will set
        # the future when a result is available.
        self.native.evaluate_javascript(
            script=javascript,
            length=len(javascript),
            world_name=None,
            source_uri=None,
            cancellable=None,
            callback=gtk_js_finished,
        )

        # wait for the future, and return the result
        return result

    def rehint(self):
        if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
            self.interface.intrinsic.width = at_least(self.interface._MIN_WIDTH)
            self.interface.intrinsic.height = at_least(self.interface._MIN_HEIGHT)
        else:  # pragma: no-cover-if-gtk3
            pass
