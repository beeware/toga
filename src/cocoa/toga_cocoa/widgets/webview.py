from rubicon.objc import objc_method
from .base import Widget
from ..libs import *


class TogaWebView(WebView):
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

        self.native.downloadDelegate = self.native
        self.native.frameLoadDelegate = self.native
        self.native.policyDelegate = self.native
        self.native.resourceLoadDelegate = self.native
        self.native.uIDelegate = self.native

        # Add the layout constraints
        self.add_constraints()

    def get_dom(self):
        # Utilises Step 2) of:
        # https://developer.apple.com/library/content/documentation/Cocoa/Conceptual/DisplayWebContent/Tasks/SaveAndLoad.html
        html = self.native.mainFrame.DOMDocument.documentElement.outerHTML  ##domDocument.markupString
        return html

    def set_url(self, value):
        if value:
            request = NSURLRequest.requestWithURL(NSURL.URLWithString(self.interface.url))
            self.native.mainFrame.loadRequest(request)

    def set_content(self, root_url, content):
        self.native.mainFrame.loadHTMLString_baseURL(content, NSURL.URLWithString(root_url))

    def set_evaluate(self, javascript):
        """
        Evaluate a JavaScript expression

        :param javascript: The javascript expression
        :type  javascript: ``str``
        """
        return self.native.stringByEvaluatingJavaScriptFromString(javascript)
