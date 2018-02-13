from rubicon.objc import objc_method
from toga_iOS.libs import UIWebView, NSURL

from .base import Widget


class TogaWebView(UIWebView):
    @objc_method
    def webView_didFinishLoadForFrame_(self, sender, frame) -> None:
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
        self.native.delegate = self.native

        # Add the layout constraints
        self.add_constraints()

    def get_dom(self):
        html = self.native.mainFrame.DOMDocument.documentElement.outerHTML
        return html

    def set_url(self, value):
        if value:
            request = NSURLRequest.requestWithURL_(NSURL.URLWithString_(self.interface.url))
            self.native.loadRequest_(request)

    def set_content(self, root_url, content):
        self.native.loadHTMLString_baseURL_(content, NSURL.URLWithString_(root_url))

    def set_user_agent(self, value):
        # self.native.customUserAgent = value if value else "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8"
        self.interface.factory.not_implemented('WebView.set_user_agent()')

    def evaluate(self, javascript):
        return self.native.stringByEvaluatingJavaScriptFromString_(javascript)

