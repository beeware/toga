from Microsoft.Web.WebView2.WinForms import WebView2

from .base import SimpleProbe


class WebViewProbe(SimpleProbe):
    native_class = WebView2

    # https://github.com/MicrosoftEdge/WebView2Feedback/issues/530
    content_supports_url = False

    # https://github.com/MicrosoftEdge/WebView2Feedback/issues/983
    javascript_supports_exception = False

    supports_on_load = True

    def extract_cookie(self, cookie_jar, name):
        return next((c for c in cookie_jar if c.name == name), None)
