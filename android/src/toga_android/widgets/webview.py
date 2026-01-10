import json
from http.cookiejar import CookieJar

from android.webkit import ValueCallback, WebView as A_WebView, WebViewClient
from java import dynamic_proxy
from java.lang import NoClassDefFoundError

from toga.widgets.webview import CookiesResult, JavaScriptResult

from .base import Widget


class ReceiveString(dynamic_proxy(ValueCallback)):
    def __init__(self, result):
        super().__init__()
        self.result = result

    def onReceiveValue(self, value):
        # If the evaluation fails, a message is written to Logcat, but the value sent to
        # the callback will be "null", with no way to distinguish it from an actual null
        # return value.
        res = json.loads(value)

        self.result.set_result(res)


class WebView(Widget):
    ON_NAVIGATION_CONFIG_MISSING_ERROR = (
        "Can't add a WebView.on_navigation_starting handler; Have you added chaquopy."
        'defaultConfig.staticProxy("toga_android.widgets.internal.webview") to the'
        "`build_gradle_extra_content` section of pyproject.toml?"
    )
    ON_LOAD_CONFIG_MISSING_ERROR = (
        "Can't add a WebView.on_webview_load handler; Have you added chaquopy."
        'defaultConfig.staticProxy("toga_android.widgets.internal.webview") to the'
        "`build_gradle_extra_content` section of pyproject.toml?"
    )

    def create(self):
        self.native = A_WebView(self._native_activity)
        self.loaded_future = None
        try:
            from .internal.webview import TogaWebClient

            self.SUPPORTS_ON_NAVIGATION_STARTING = True
            self.SUPPORTS_ON_WEBVIEW_LOAD = True
            client = TogaWebClient(self)
        except NoClassDefFoundError:  # pragma: no cover
            # Briefcase configuration hasn't declared a static proxy
            self.SUPPORTS_ON_NAVIGATION_STARTING = False
            self.SUPPORTS_ON_WEBVIEW_LOAD = False
            client = WebViewClient()

        # Set a WebViewClient so that new links open in this activity,
        # rather than triggering the phone's web browser.
        self.native.setWebViewClient(client)

        self.settings = self.native.getSettings()
        self.default_user_agent = self.settings.getUserAgentString()
        self.settings.setJavaScriptEnabled(True)
        self.settings.setDomStorageEnabled(True)
        # enable pinch-to-zoom without the deprecated on-screen controls
        self.settings.setBuiltInZoomControls(True)
        self.settings.setDisplayZoomControls(False)

    def get_url(self):
        url = self.native.getUrl()
        if url == "about:blank" or url.startswith("data:"):
            return None
        else:
            return url

    def set_url(self, value, future=None):
        if value is None:
            value = "about:blank"
        self.loaded_future = future
        self.native.loadUrl(value)

    def set_content(self, root_url, content):
        # There is a loadDataWithBaseURL method, but it's inconsistent about whether
        # getUrl returns the given URL or a data: URL. Rather than support this feature
        # intermittently, it's better to not support it at all.
        self.native.loadData(content, "text/html", "utf-8")

    def get_user_agent(self):
        return self.settings.getUserAgentString()

    def set_user_agent(self, value):
        self.settings.setUserAgentString(
            self.default_user_agent if value is None else value
        )

    def get_cookies(self):
        # Create the result object
        result = CookiesResult()
        result.set_result(CookieJar())

        # Signal that this feature is not implemented on the current platform
        self.interface.factory.not_implemented("webview.cookies")

        return result

    def evaluate_javascript(self, javascript, on_result=None):
        result = JavaScriptResult(on_result)

        self.native.evaluateJavascript(javascript, ReceiveString(result))
        return result
