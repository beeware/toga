from toga_gtk.libs import WebKit2

from .base import SimpleProbe


class WebViewProbe(SimpleProbe):
    native_class = WebKit2.WebView
    content_supports_url = True
    javascript_supports_exception = True
    supports_on_load = True
