import asyncio
import base64

from travertino.size import at_least

from ..libs.android.view import Gravity, View__MeasureSpec
from ..libs.android.webkit import ValueCallback, WebView as A_WebView, WebViewClient
from .base import Widget, align


class ReceiveString(ValueCallback):
    def __init__(self, fn=None):
        super().__init__()
        self._fn = fn

    def onReceiveValue(self, value):
        if self._fn:
            if value is None:
                self._fn(None)
            else:
                # Ensure we send a string to the function.
                self._fn(value.toString())


class WebView(Widget):
    def create(self):
        self.native = A_WebView(self._native_activity)
        # Set a WebViewClient so that new links open in this activity,
        # rather than triggering the phone's web browser.
        self.native.setWebViewClient(WebViewClient())
        # Enable JS.
        self.native.getSettings().setJavaScriptEnabled(True)

    def set_on_key_down(self, handler):
        # Android isn't a platform that usually has a keyboard attached, so this is unimplemented for now.
        self.interface.factory.not_implemented('WebView.set_on_key_down()')

    def set_on_webview_load(self, handler):
        # This requires subclassing WebViewClient, which is not yet possible with rubicon-java.
        self.interface.factory.not_implemented('WebView.set_on_webview_load()')

    def get_dom(self):
        # Android has no straightforward way to get the DOM from the browser synchronously.
        self.interface.factory.not_implemented('WebView.get_dom()')

    def get_url(self):
        return self.native.getUrl()

    def set_url(self, value):
        if value:
            self.native.loadUrl(str(value))

    def set_content(self, root_url, content):
        # Android WebView lacks an underlying set_content() primitive, so we navigate to
        # a data URL. This means we ignore the root_url parameter.
        data_url = (
            "data:text/html; charset=utf-8; base64," +
            base64.b64encode(content.encode('utf-8')).decode('ascii')
        )
        self.set_url(data_url)

    def set_user_agent(self, value):
        if value is not None:
            self.native.getSettings().setUserAgentString(value)

    async def evaluate_javascript(self, javascript):
        js_value = asyncio.Future()
        self.native.evaluateJavascript(str(javascript), ReceiveString(js_value.set_result))
        return await js_value

    def invoke_javascript(self, javascript):
        self.native.evaluateJavascript(str(javascript), ReceiveString())

    def set_alignment(self, value):
        # Refuse to set alignment unless widget has been added to a container.
        # This is because this widget's setGravity() requires LayoutParams before it can be called.
        if not self.native.getLayoutParams():
            return
        self.native.setGravity(Gravity.CENTER_VERTICAL | align(value))

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface.MIN_WIDTH)
        # Refuse to call measure() if widget has no container, i.e., has no LayoutParams.
        # Android's measure() throws NullPointerException if the widget has no LayoutParams.
        if not self.native.getLayoutParams():
            return
        self.native.measure(
            View__MeasureSpec.UNSPECIFIED,
            View__MeasureSpec.UNSPECIFIED,
        )
        self.interface.intrinsic.width = at_least(self.native.getMeasuredWidth())
        self.interface.intrinsic.height = self.native.getMeasuredHeight()
