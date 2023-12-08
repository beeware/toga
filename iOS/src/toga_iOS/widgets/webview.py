from rubicon.objc import objc_id, objc_method, objc_property, py_from_ns
from travertino.size import at_least

from toga.widgets.webview import JavaScriptResult
from toga_iOS.libs import NSURL, NSURLRequest, WKWebView
from toga_iOS.widgets.base import Widget


def js_completion_handler(result):
    def _completion_handler(res: objc_id, error: objc_id) -> None:
        if error:
            error = py_from_ns(error)
            exc = RuntimeError(str(error))
            result.set_exception(exc)
        else:
            result.set_result(py_from_ns(res))

    return _completion_handler


class TogaWebView(WKWebView):
    interface = objc_property(object, weak=True)
    impl = objc_property(object, weak=True)

    @objc_method
    def webView_didFinishNavigation_(self, navigation) -> None:
        self.interface.on_webview_load()

        if self.impl.loaded_future:
            self.impl.loaded_future.set_result(None)
            self.impl.loaded_future = None


class WebView(Widget):
    def create(self):
        self.native = TogaWebView.alloc().init()
        self.native.interface = self.interface
        self.native.impl = self

        # Enable the content inspector. This was added in iOS 16.4.
        # It is a no-op on earlier versions.
        self.native.inspectable = True
        self.native.navigationDelegate = self.native

        self.loaded_future = None

        # Add the layout constraints
        self.add_constraints()

    def get_url(self):
        url = str(self.native.URL)
        return None if url == "about:blank" else url

    def set_url(self, value, future=None):
        if value:
            request = NSURLRequest.requestWithURL(NSURL.URLWithString(value))
        else:
            request = NSURLRequest.requestWithURL(NSURL.URLWithString("about:blank"))

        self.loaded_future = future
        self.native.loadRequest(request)

    def set_content(self, root_url, content):
        self.native.loadHTMLString(content, baseURL=NSURL.URLWithString(root_url))

    def get_user_agent(self):
        return str(self.native.valueForKey("userAgent"))

    def set_user_agent(self, value):
        self.native.customUserAgent = value

    def evaluate_javascript(self, javascript, on_result=None):
        result = JavaScriptResult(on_result)
        self.native.evaluateJavaScript(
            javascript,
            completionHandler=js_completion_handler(result),
        )

        return result

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface._MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface._MIN_HEIGHT)
