from rubicon.objc import objc_method

from toga_iOS.libs import NSURL, NSURLRequest, WKWebView
from toga_iOS.widgets.base import Widget


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
        if self.interface.on_key_down:
            self.interface.on_key_down(event.keyCode, event.modifierFlags)


class WebView(Widget):
    def create(self):
        self.native = TogaWebView.alloc().init()
        self.native.interface = self.interface
        self.native.delegate = self.native

        # Add the layout constraints
        self.add_constraints()

    def set_on_key_down(self, handler):
        pass

    def set_on_webview_load(self, handler):
        pass

    def get_dom(self):
        html = self.native.DOMDocument.documentElement.outerHTML
        return html

    def set_url(self, value):
        if value:
            if self.interface.url.startswith('file://'):
                url = NSURL.fileURLWithPath(self.interface.url[7:])
            else:
                url = NSURL.URLWithString(self.interface.url)

            request = NSURLRequest.requestWithURL_(url)
            self.native.loadRequest_(request)

    def set_content(self, root_url, content):
        self.native.loadHTMLString_baseURL_(content, NSURL.URLWithString_(root_url))

    def set_user_agent(self, value):
        # user_agent = value if value else "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8"  # NOQA
        # self.native.customUserAgent = user_agent
        self.interface.factory.not_implemented('WebView.set_user_agent()')

    async def evaluate_javascript(self, javascript):
        return self.native.stringByEvaluatingJavaScriptFromString_(javascript)

    def invoke_javascript(self, javascript):
        return self.native.stringByEvaluatingJavaScriptFromString_(javascript)
