import os
import urllib

from PySide6.QtWebEngineWidgets import QWebEngineView

from .base import SimpleProbe


class WebViewProbe(SimpleProbe):
    native_class = QWebEngineView

    # See #4415. Qt's Webview *does* support content URLs; however, there appears to be
    # a bug with Qt's WebView that causes the URL to be returned as a `data:text/html`
    # content URL rather than the requested URL. As a workaround for test reliability,
    # disable tests for content URLs.
    # content_supports_url = True
    content_supports_url = False
    javascript_supports_exception = True
    supports_on_load = True

    def extract_cookie(self, cookie_jar, name):
        return next((c for c in cookie_jar if c.name == name), None)

    def get_large_content_url(self, widget):
        for f in os.listdir(widget._impl._large_content_dir):
            p = widget._impl._large_content_dir / f
        return urllib.parse.unquote(p.as_uri())
