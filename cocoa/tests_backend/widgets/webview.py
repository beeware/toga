from toga_cocoa.libs import WKWebView

from .base import SimpleProbe


class WebViewProbe(SimpleProbe):
    native_class = WKWebView
    content_supports_url = True
    javascript_supports_exception = True
    supports_on_load = True
