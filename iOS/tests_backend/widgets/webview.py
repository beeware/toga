from toga_iOS.libs import WKWebView

from .base import SimpleProbe


class WebViewProbe(SimpleProbe):
    native_class = WKWebView
    content_supports_url = True
    javascript_supports_exception = True
    supports_on_load = True

    @property
    def has_focus(self):
        # iOS has an inner, private WKContentView object that actually becomes
        # the first responder. However, we can't get access to that object,
        # and we can't navigate from that object back to the WKWebView.
        # So, we do a weak check that the class name of the first responder
        # is a WKContentView, and rely on the fact that the tests don't ever
        # put 2 WKContentViews on the page at once.
        current = self.widget.window._impl.native.firstResponder()
        return current.objc_class.name == "WKContentView"
