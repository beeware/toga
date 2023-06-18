from android.webkit import WebView

from .base import SimpleProbe


class WebViewProbe(SimpleProbe):
    native_class = WebView
    content_supports_url = False
    javascript_supports_exception = False
    supports_on_load = False
