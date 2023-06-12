import json

from travertino.size import at_least

from toga.widgets.webview import JavaScriptResult

from ..libs.android.webkit import ValueCallback, WebView as A_WebView, WebViewClient
from .base import Widget


class ReceiveString(ValueCallback):
    def __init__(self, future, on_result):
        super().__init__()
        self.future = future
        self.on_result = on_result

    def onReceiveValue(self, value):
        # If the evaluation fails, a message is written to Logcat, but the value sent to
        # the callback will be "null", with no way to distinguish it from an actual null
        # return value.
        result = json.loads(value)
        self.future.set_result(result)
        if self.on_result:
            self.on_result(result)


class WebView(Widget):
    def create(self):
        self.native = A_WebView(self._native_activity)
        # Set a WebViewClient so that new links open in this activity,
        # rather than triggering the phone's web browser.
        self.native.setWebViewClient(WebViewClient())

        self.settings = self.native.getSettings()
        self.default_user_agent = self.settings.getUserAgentString()
        self.settings.setJavaScriptEnabled(True)

    def get_url(self):
        url = self.native.getUrl()
        return None if url == "about:blank" else url

    def set_url(self, value, future=None):
        if value is None:
            value = "about:blank"
        self.native.loadUrl(value)

        # Detecting when the load is complete requires subclassing WebViewClient
        # (https://github.com/beeware/toga/issues/1020).
        if future:
            future.set_result(None)

    def set_content(self, root_url, content):
        self.native.loadDataWithBaseURL(
            root_url,  # baseUrl
            content,
            "text/html",
            "utf-8",
            root_url,  # historyUrl
        )

    def get_user_agent(self):
        return self.settings.getUserAgentString()

    def set_user_agent(self, value):
        self.settings.setUserAgentString(
            self.default_user_agent if value is None else value
        )

    def evaluate_javascript(self, javascript, on_result=None):
        result = JavaScriptResult()

        self.native.evaluateJavascript(
            javascript, ReceiveString(result.future, on_result)
        )
        return result

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface._MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface._MIN_HEIGHT)
