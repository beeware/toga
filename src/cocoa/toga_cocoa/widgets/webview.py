from rubicon.objc import objc_method
from .base import Widget
from ..libs import *


class TogaWebView(WebView):
    @objc_method
    def webView_didFinishLoadForFrame_(self, sender, frame) -> None:
        print ("FINISHED LOADING")
        pass

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

        self.native.setDownloadDelegate_(self.native)
        self.native.setFrameLoadDelegate_(self.native)
        self.native.setPolicyDelegate_(self.native)
        self.native.setResourceLoadDelegate_(self.native)
        self.native.setUIDelegate_(self.native)

        # Add the layout constraints
        self.add_constraints()

    def set_url(self, value):
        if value:
            request = NSURLRequest.requestWithURL_(NSURL.URLWithString_(self.interface.url))
            self.native.mainFrame.loadRequest_(request)

    def set_content(self, root_url, content):
        self.native.mainFrame.loadHTMLString_baseURL_(content, NSURL.URLWithString_(root_url))

    def evaluate(self, javascript):
        """
        Evaluate a JavaScript expression

        :param javascript: The javascript expression
        :type  javascript: ``str``
        """
        return self.native.stringByEvaluatingJavaScriptFromString_(javascript)
