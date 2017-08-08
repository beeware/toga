from rubicon.objc import objc_method

from toga.interface import WebView as WebViewInterface

from .base import WidgetMixin
from ..libs import *


class TogaWebView(WebView):
    @objc_method
    def webView_didFinishLoadForFrame_(self, sender, frame) -> None:
        if self._interface.on_webview_load:
            self._interface.on_webview_load(self._interface)

    @objc_method
    def acceptsFirstResponder(self) -> bool:
        return True

    @objc_method
    def keyDown_(self, event) -> None:
        if self._interface.on_key_down:
            self._interface.on_key_down(event.keyCode, event.modifierFlags)


class WebView(WebViewInterface, WidgetMixin):
    def __init__(self, id=None, style=None, url=None, on_key_down=None, on_webview_load=None):
        super().__init__(id=id, style=style, url=url, on_key_down=on_key_down, on_webview_load=on_webview_load)
        self._create()

    def create(self):
        self._impl = TogaWebView.alloc().init()
        self._impl._interface = self

        self._impl.setDownloadDelegate_(self._impl)
        self._impl.setFrameLoadDelegate_(self._impl)
        self._impl.setPolicyDelegate_(self._impl)
        self._impl.setResourceLoadDelegate_(self._impl)
        self._impl.setUIDelegate_(self._impl)

        # Add the layout constraints
        self._add_constraints()

    def _get_dom(self):
        # Utilises Step 2) of:
        # https://developer.apple.com/library/content/documentation/Cocoa/Conceptual/DisplayWebContent/Tasks/SaveAndLoad.html
        html = self._impl.mainFrame.DOMDocument.documentElement.outerHTML ##domDocument.markupString
        return html

    def _set_url(self, value):
        if value:
            request = NSURLRequest.requestWithURL_(NSURL.URLWithString_(self._url))
            self._impl.mainFrame.loadRequest_(request)

    def _set_content(self, root_url, content):
        self._impl.mainFrame.loadHTMLString_baseURL_(content, NSURL.URLWithString_(root_url))

    def evaluate(self, javascript):
        return self._impl.stringByEvaluatingJavaScriptFromString_(javascript)
