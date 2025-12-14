from http.cookiejar import CookieJar

from android.webkit import WebView
from pytest import skip

from .base import SimpleProbe


class WebViewProbe(SimpleProbe):
    native_class = WebView
    content_supports_url = False
    javascript_supports_exception = False
    supports_on_load = False

    def extract_cookie(self, cookie_jar, name):
        assert isinstance(cookie_jar, CookieJar)
        skip("Cookie retrieval not implemented on Android")
