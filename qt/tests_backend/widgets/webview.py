import os
import urllib

import pytest
from PySide6.QtWebEngineWidgets import QWebEngineView

from .base import SimpleProbe


class WebViewProbe(SimpleProbe):
    native_class = QWebEngineView
    content_supports_url = True
    javascript_supports_exception = True
    supports_on_load = True

    def extract_cookie(self, cookie_jar, name):
        return next((c for c in cookie_jar if c.name == name), None)

    def get_large_content_url(self, widget):
        for f in os.listdir(widget._impl._large_content_dir):
            p = widget._impl._large_content_dir / f
        return urllib.parse.unquote(p.as_uri())

    def assert_system_effects_top(self, expected, root):
        pytest.xfail("Qt does not currently apply effects over top bar")
