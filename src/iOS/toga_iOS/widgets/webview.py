from rubicon.objc import objc_method

from toga_iOS.libs import *

from .base import Widget

from concurrent.futures import Future


class TogaUIWebView(UIWebView):
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


class WebKit1WebView(Widget):
    def create(self):
        self.native = TogaUIWebView.alloc().init()
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
        pass

    def evaluate(self, javascript):
        return self.native.stringByEvaluatingJavaScriptFromString_(javascript)


if "WKWebView" in vars():
    class TogaWKWebView(WKWebView):
        @objc_method
        def webView_didFinish_(self, navi):
            if self.interface.on_webview_load:
            self.interface.on_webview_load(self.interface)

        @objc_method
        def acceptsFirstResponder(self) -> bool:
            return True

        @objc_method
        def keyDown_(self, event) -> None:
            print('in keyDown', event.keyCode)
            if self.interface.on_key_down:
                self.interface.on_key_down(event.keyCode, event.modifierFlags)

        @objc_method
        def touchBar(self):
            # Disable the touchbar.
            return None

    class WebKit2WebView(Widget):
        def create(self):
            self.native = TogaWKWebView.alloc().init()
            self.native.interface = self.interface

            self.native.uiDelegate = self.native
            self.native.navigationDelegate = self.native

            self.add_constraints()

        def get_dom(self):
            return self.evaluate(
                'document.getElementsByTagName("html")[0].outerHTML')

        def set_url(self, value):
            if value:
                self.interface.url = value

            request = NSURLRequest.requestWithURL(NSURL.URLWithString(
                self.interface.url))
            self.native.load(request)

        def set_content(self, root_url, content):
            self.native.loadHTMLString_baseURL_(
                content, NSURL.URLWithString(root_url))

        def set_user_agent(self, value):
            self.native.customUserAgent = value

        def evaluate(self, js_str):
            fur = Future()  # type: concurrent.futures.Future

            def when_finish(result, err):
                if fur.done():
                    return

                if err:
                    fur.set_exception(err)

                else:
                    fur.set_result(result)

            self.native.evaluateJavaScript_completionHandler_(
                js_str, when_finish)

            return fur

    WebView = WebKit2WebView

else:
    WebView = WebKit1WebView
