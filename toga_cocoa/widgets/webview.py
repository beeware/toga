from rubicon.objc import objc_method

from .base import Widget
from ..libs import *


class TogaWebView(WebView):
    @objc_method
    def webView_didFinishLoadForFrame_(self, sender, frame) -> None:
        # print ("FINISHED LOADING")
        pass


class WebView(Widget):
    def __init__(self, url=None, style=None):
        super(WebView, self).__init__(style=style)

        self.startup()

        self.url = url

    def startup(self):
        self._impl = TogaWebView.alloc().init()

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

    def _apply_layout(self, layout):
        # When you change the frame of the webview, you also need to chnge
        # the size of the main frame that is part of the webview.
        frame = NSRect(NSPoint(layout.left, layout.top), NSSize(layout.width, layout.height))
        self._impl.setFrame_(frame)
        self._impl.mainFrame.frameView.setFrameSize_(frame.size)
