from rubicon.objc import objc_method

from .base import Widget
from ..libs import *


class TogaWebView(WebView):
    @objc_method
    def webView_didFinishLoadForFrame_(self, sender, frame) -> None:
        # print ("FINISHED LOADING")
        pass

    @objc_method
    def acceptsFirstResponder(self) -> bool:
        return True

    @objc_method
    def keyDown_(self, event) -> None:
        if self._interface.on_key_down:
            self._interface.on_key_down(event.keyCode, event.modifierFlags)


class WebView(Widget):
    def __init__(self, url=None, style=None, on_key_down=None):
        super(WebView, self).__init__(style=style)

        self.on_key_down = on_key_down

        self.startup()

        self.url = url

    def startup(self):
        self._impl = TogaWebView.alloc().init()
        self._impl._interface = self

        self._impl.setDownloadDelegate_(self._impl)
        self._impl.setFrameLoadDelegate_(self._impl)
        self._impl.setPolicyDelegate_(self._impl)
        self._impl.setResourceLoadDelegate_(self._impl)
        self._impl.setUIDelegate_(self._impl)

        # Disable all autolayout functionality
        self._impl.setTranslatesAutoresizingMaskIntoConstraints_(False)
        self._impl.setAutoresizesSubviews_(False)

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value
        if value:
            request = NSURLRequest.requestWithURL_(NSURL.URLWithString_(self._url))
            self._impl.mainFrame.loadRequest_(request)

    def set_content(self, root_url, content):
        self._url = root_url
        self._impl.mainFrame.loadHTMLString_baseURL_(content, NSURL.URLWithString_(root_url))

    def evaluate(self, javascript):
        return self._impl.stringByEvaluatingJavaScriptFromString_(javascript)

    def _apply_layout(self, layout):
        # When you change the frame of the webview, you also need to chnge
        # the size of the main frame that is part of the webview.
        frame = NSRect(NSPoint(layout.left, layout.top), NSSize(layout.width, layout.height))
        self._impl.setFrame_(frame)
        self._impl.mainFrame.frameView.setFrameSize_(frame.size)
