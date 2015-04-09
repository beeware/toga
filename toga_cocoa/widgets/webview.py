from __future__ import print_function, absolute_import, division

from rubicon.objc import objc_method

from .base import Widget
from ..libs import *


class WebViewImpl(WebView):
    @objc_method('v@@')
    def webView_didFinishLoadForFrame_(self, sender, frame):
        print ("FINISHED LOADING")
        pass


class WebView(Widget):
    def __init__(self, url=None, **style):
        super(WebView, self).__init__(**style)

        self.startup()

        # self.url = url

    def startup(self):
        self._impl = WebViewImpl.alloc().init()

        self._impl.setDownloadDelegate_(self._impl)
        self._impl.setFrameLoadDelegate_(self._impl)
        self._impl.setPolicyDelegate_(self._impl)
        self._impl.setResourceLoadDelegate_(self._impl)
        self._impl.setUIDelegate_(self._impl)
        # Disable all autolayout functionality
        # self._impl.mainFrame().frameView().documentView().setTranslatesAutoresizingMaskIntoConstraints_(True)
        # self._impl.mainFrame().frameView().setTranslatesAutoresizingMaskIntoConstraints_(True)
        # self._impl.mainFrame().frameView().setAllowsScrolling_(False)
        # self._impl.setTranslatesAutoresizingMaskIntoConstraints_(True)
        self._impl.setTranslatesAutoresizingMaskIntoConstraints_(False)

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value
        if value:
            request = NSURLRequest.requestWithURL_(NSURL.URLWithString_(self._url))
            self._impl.mainFrame().loadRequest_(request)

    def _set_frame(self, frame):
        print ("CUSTOM WEB FRAME", (self._impl.frame.size.width, self._impl.frame.size.height), (self._impl.frame.origin.x, self._impl.frame.origin.y))
        print ("FRAMEVIEW ", (self._impl.mainFrame().frameView().frame.size.width, self._impl.mainFrame().frameView().frame.size.height), (self._impl.mainFrame().frameView().frame.origin.x, self._impl.mainFrame().frameView().frame.origin.y))
        print ("DOCUMENTVIEW ", (self._impl.mainFrame().frameView().documentView().frame.size.width, self._impl.mainFrame().frameView().documentView().frame.size.height), (self._impl.mainFrame().frameView().documentView().frame.origin.x, self._impl.mainFrame().frameView().documentView().frame.origin.y))

        # self._impl.setFrame_(NSRect(NSPoint(50, 100), NSSize(300 ,200)))
        # self._impl.setFrame_(NSRect(NSPoint(frame.origin.x + 50, 100), NSSize(300,200)))
        # self._impl.setFrame_(NSRect(NSPoint(frame.origin.x, frame.origin.y), NSSize(300,200)))
        # self._impl.setFrame_(NSRect(NSPoint(frame.origin.x, frame.origin.y), NSSize(300 ,frame.size.height)))
        # self._impl.setFrame_(NSRect(NSPoint(frame.origin.x, frame.origin.y), NSSize(700 ,frame.size.height)))
        # self._set_frame(NSRect(NSPoint(layout.left, layout.top), NSSize(layout.width, layout.height)))

        self._impl.setFrame_(frame)
        # self._impl.UIDelegate.webView_setFrame_(self._impl, frame)
        # self._impl.setNeedsDisplay_(True)
        # self._impl.mainFrame().frameView().documentView().setNeedsDisplay_(True)
        # self._impl.mainFrame().frameView().setFrame_(frame)
        # self._impl.mainFrame().frameView().documentView().setFrame_(frame)

        print ("POST CUSTOM WEB FRAME", (self._impl.frame.size.width, self._impl.frame.size.height), (self._impl.frame.origin.x, self._impl.frame.origin.y))
        print ("POST FRAMEVIEW ", (self._impl.mainFrame().frameView().frame.size.width, self._impl.mainFrame().frameView().frame.size.height), (self._impl.mainFrame().frameView().frame.origin.x, self._impl.mainFrame().frameView().frame.origin.y))
        print ("POST DOCUMENTVIEW ", (self._impl.mainFrame().frameView().documentView().frame.size.width, self._impl.mainFrame().frameView().documentView().frame.size.height), (self._impl.mainFrame().frameView().documentView().frame.origin.x, self._impl.mainFrame().frameView().documentView().frame.origin.y))
