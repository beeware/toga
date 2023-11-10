from travertino.size import at_least

from toga.widgets.webview import JavaScriptResult

from .base import Widget


class WebView(Widget):
    def create(self):
        self.native = self._create_native_widget("iframe")

    def get_url(self):
        url = str(self.native.src)
        return None if url == "about:blank" else url

    def set_url(self, value, future=None):
        if value:
            self.native.src = value
        else:
            self.native.src = "about:blank"

        self.loaded_future = future

    def set_content(self, root_url, content):
        pass
        # self.native.loadHTMLString(content, baseURL=NSURL.URLWithString(root_url))

    def get_user_agent(self):
        # return str(self.native.valueForKey("userAgent"))
        return "user agent?"

    def set_user_agent(self, value):
        # self.native.customUserAgent = value
        pass

    def evaluate_javascript(self, javascript: str, on_result=None) -> str:
        result = JavaScriptResult()

        return result

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface._MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface._MIN_HEIGHT)
