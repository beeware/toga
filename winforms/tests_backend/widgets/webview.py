import os
import urllib

from Microsoft.Web.WebView2.WinForms import WebView2

from .base import SimpleProbe


class WebViewProbe(SimpleProbe):
    native_class = WebView2

    # https://github.com/MicrosoftEdge/WebView2Feedback/issues/530
    content_supports_url = False

    # https://github.com/MicrosoftEdge/WebView2Feedback/issues/983
    javascript_supports_exception = False

    supports_on_load = True
    supports_on_navigation_starting = True

    def extract_cookie(self, cookie_jar, name):
        return next((c for c in cookie_jar if c.name == name), None)

    def get_large_content_url(self, widget):
        for f in os.listdir(widget._impl._large_content_dir):
            p = widget._impl._large_content_dir / f
        return urllib.parse.unquote(p.as_uri())
