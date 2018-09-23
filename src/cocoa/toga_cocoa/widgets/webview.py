from travertino.size import at_least
from rubicon.objc import objc_method

from toga_cocoa.keys import toga_key
from toga_cocoa.libs import NSURL, NSURLRequest, WKWebView

from .base import Widget


class TogaWebView(WKWebView):
    @objc_method
    def webView_didFinishLoadForFrame_(self, sender, frame) -> None:
        if self.interface.on_webview_load:
            self.interface.on_webview_load(self.interface)

    @objc_method
    def acceptsFirstResponder(self) -> bool:
        return True

    @objc_method
    def keyDown_(self, event) -> None:
        print('in keyDown', event.keyCode)
        if self.interface.on_key_down:
            self.interface.on_key_down(**toga_key(event))

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

    def get_dom(self):
        # Utilises Step 2) of:
        # https://developer.apple.com/library/content/documentation/
        #       Cocoa/Conceptual/DisplayWebContent/Tasks/SaveAndLoad.html
        html = self.native.DOMDocument.documentElement.outerHTML
        return html

    def set_url(self, value):
        if value:
            request = NSURLRequest.requestWithURL(NSURL.URLWithString(self.interface.url))
            self.native.loadRequest(request)

    def set_content(self, root_url, content):
        self.native.loadHTMLString_baseURL_(content, NSURL.URLWithString(root_url))

    def set_user_agent(self, value):
        self.native.customUserAgent = value if value else "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8"

    def evaluate(self, javascript):
        """
        Evaluate a JavaScript expression

        :param javascript: The javascript expression
        :type  javascript: ``str``
        """
        return self.native.stringByEvaluatingJavaScriptFromString(javascript)

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface.MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface.MIN_HEIGHT)
