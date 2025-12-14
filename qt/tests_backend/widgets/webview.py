from PySide6.QtWebEngineWidgets import QWebEngineView

from .base import SimpleProbe


class WebViewProbe(SimpleProbe):
    native_class = QWebEngineView
    content_supports_url = True
    javascript_supports_exception = True
    supports_on_load = True

    def extract_cookie(self, cookie_jar, name):
        return next((c for c in cookie_jar if c.name == name), None)
