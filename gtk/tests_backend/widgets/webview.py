from http.cookiejar import CookieJar

import pytest
from pytest import skip

from toga_gtk.libs import GTK_VERSION, WebKit2

from .base import SimpleProbe


class WebViewProbe(SimpleProbe):
    native_class = WebKit2.WebView
    content_supports_url = True
    javascript_supports_exception = True
    supports_on_load = True

    if GTK_VERSION >= (4, 0, 0):
        pytest.skip("GTK4 doesn't support trees yet")

    def extract_cookie(self, cookie_jar, name):
        assert isinstance(cookie_jar, CookieJar)
        skip("Cookie retrieval not implemented on GTK")
