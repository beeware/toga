import os
from http.cookiejar import CookieJar

import pytest
from android.webkit import WebView
from pytest import skip

from .base import SimpleProbe


class WebViewProbe(SimpleProbe):
    native_class = WebView
    content_supports_url = False
    javascript_supports_exception = False
    supports_on_load = True

    def extract_cookie(self, cookie_jar, name):
        assert isinstance(cookie_jar, CookieJar)
        skip("Cookie retrieval not implemented on Android")

    def get_large_content_url(self, widget):
        for f in os.listdir(widget._impl._large_content_dir):
            url = widget._impl._large_content_base_url + f
        return url

    def assert_system_effects_top(self, expected, root):
        pytest.skip("Android does not currently apply effects over navigation bar")
