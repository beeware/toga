from __future__ import print_function, absolute_import, division


from .base import Widget
from ..libs import *


class WebView_impl(object):
    WebViewImpl = ObjCSubclass('WebView', 'WebViewImpl')

    @WebViewImpl.method('v@@')
    def webView_didFinishLoadForFrame_(self, sender, frame):
        pass

WebViewImpl = ObjCClass('WebViewImpl')


class WebView(Widget):
    def __init__(self, url=None):
        super(WebView, self).__init__()

        self.startup()

        self.url = url

    def startup(self):
        self._impl = WebViewImpl.alloc().init()

        self._impl.setDownloadDelegate_(self._impl)
        self._impl.setFrameLoadDelegate_(self._impl)
        self._impl.setPolicyDelegate_(self._impl)
        self._impl.setResourceLoadDelegate_(self._impl)
        self._impl.setUIDelegate_(self._impl)
        self._impl.setTranslatesAutoresizingMaskIntoConstraints_(False)

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value
        if value:
            request = NSURLRequest.requestWithURL_(NSURL.URLWithString_(get_NSString(self._url)))
            self._impl.mainFrame().loadRequest_(request)
