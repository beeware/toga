from asyncio import get_event_loop

from rubicon.objc import objc_method, objc_property, py_from_ns
from rubicon.objc.runtime import objc_id

from toga_iOS.libs import NSURL, NSURLRequest, WKWebView
from toga_iOS.widgets.base import Widget


class TogaWebView(WKWebView):
    interface = objc_property(object, weak=True)
    impl = objc_property(object, weak=True)

    @objc_method
    def webView_didFinishNavigation_(self, navigation) -> None:
        if self.interface.on_webview_load:
            self.interface.on_webview_load(self.interface)

    @objc_method
    def acceptsFirstResponder(self) -> bool:
        return True

    @objc_method
    def keyDown_(self, event) -> None:
        if self.interface.on_key_down:
            self.interface.on_key_down(event.keyCode, event.modifierFlags)


class WebView(Widget):
    def create(self):
        self.native = TogaWebView.alloc().init()
        self.native.interface = self.interface
        self.native.impl = self

        self.native.navigationDelegate = self.native
        self.native.uIDelegate = self.native

        # Add the layout constraints
        self.add_constraints()

    def set_on_key_down(self, handler):
        pass

    def set_on_webview_load(self, handler):
        pass

    def get_dom(self):
        html = self.native.DOMDocument.documentElement.outerHTML
        return html

    def get_url(self):
        url = self.native.URL
        if url:
            return str(url)

    def set_url(self, value):
        if value:
            request = NSURLRequest.requestWithURL(NSURL.URLWithString(value))
            self.native.loadRequest(request)

    def set_content(self, root_url, content):
        self.native.loadHTMLString(content, baseURL=NSURL.URLWithString(root_url))

    def set_user_agent(self, value):
        user_agent = value if value else "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8"  # NOQA
        self.native.customUserAgent = user_agent

    async def evaluate_javascript(self, javascript):
        loop = get_event_loop()
        future = loop.create_future()

        def completion_handler(res: objc_id, error: objc_id) -> None:

            if error:
                error = py_from_ns(error)
                exc = RuntimeError(str(error))
                future.set_exception(exc)
            else:
                future.set_result(py_from_ns(res))

        self.native.evaluateJavaScript(javascript, completionHandler=completion_handler)

        return await future

    def invoke_javascript(self, javascript):
        self.native.evaluateJavaScript(javascript, completionHandler=None)
