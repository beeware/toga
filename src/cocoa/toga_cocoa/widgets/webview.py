from asyncio import get_event_loop

from travertino.size import at_least

from toga_cocoa.keys import toga_key
from toga_cocoa.libs import NSURL, NSURLRequest, WKWebView
from rubicon.objc import objc_method, py_from_ns, send_super
from rubicon.objc.runtime import objc_id

from .base import Widget


class TogaWebView(WKWebView):
    @objc_method
    def webView_didFinish_navigation_(self, sender, wkNavigation) -> None:
        if self.interface.on_webview_load:
            self.interface.on_webview_load(self.interface)

    @objc_method
    def acceptsFirstResponder(self) -> bool:
        return True

    @objc_method
    def keyDown_(self, event) -> None:
        if self.interface.on_key_down:
            self.interface.on_key_down(self.interface, **toga_key(event))
        send_super(__class__, self, 'keyDown:', event)

    @objc_method
    def touchBar(self):
        # Disable the touchbar.
        return None


class WebView(Widget):
    def create(self):
        self.native = TogaWebView.alloc().init()
        self.native.interface = self.interface

        self.native.downloadDelegate = self.native
        self.native.frameLoadDelegate = self.native
        self.native.policyDelegate = self.native
        self.native.resourceLoadDelegate = self.native
        self.native.uIDelegate = self.native

        # Add the layout constraints
        self.add_constraints()

    def set_on_key_down(self, handler):
        pass

    def set_on_webview_load(self, handler):
        pass

    def get_dom(self):
        # Utilises Step 2) of:
        # https://developer.apple.com/library/content/documentation/
        #       Cocoa/Conceptual/DisplayWebContent/Tasks/SaveAndLoad.html
        html = self.native.mainframe.DOMDocument.documentElement.outerHTML
        return html

    def set_url(self, value):
        if value:
            request = NSURLRequest.requestWithURL(NSURL.URLWithString(self.interface.url))
            self.native.loadRequest(request)

    def set_content(self, root_url, content):
        self.native.loadHTMLString(content, baseURL=NSURL.URLWithString(root_url))

    def set_user_agent(self, value):
        user_agent = value if value else "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8"  # NOQA
        self.native.customUserAgent = user_agent

    async def evaluate_javascript(self, javascript):
        """
        Evaluate a JavaScript expression.

        **This method is asynchronous**. It will return when the expression has been
        evaluated and a result is available.

        :param javascript: The javascript expression to evaluate
        :type  javascript: ``str``
        """

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
        """
        Invoke a block of javascript.

        :param javascript: The javascript expression to invoke
        """
        self.native.evaluateJavaScript(javascript, completionHandler=None)

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface.MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface.MIN_HEIGHT)
