from http.cookiejar import CookieJar

from pytest import skip

from toga_gtk.libs import WebKit2

from .base import SimpleProbe


class WebViewProbe(SimpleProbe):
    native_class = WebKit2.WebView
    content_supports_url = True
    javascript_supports_exception = True
    supports_on_load = True

    def extract_cookie(self, cookie_jar, name):
        assert isinstance(cookie_jar, CookieJar)
        skip("Cookie retrieval not implemented on GTK")
