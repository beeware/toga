import pytest

from toga_cocoa.libs import WKWebView

from .base import SimpleProbe


class WebViewProbe(SimpleProbe):
    native_class = WKWebView
    content_supports_url = True
    javascript_supports_exception = True
    supports_on_load = True

    def extract_cookie(self, cookie_jar, name):
        return next((c for c in cookie_jar if c.name == name), None)

    def assert_system_effects_top(self, expected, root):
        pytest.skip("Cocoa baceknd currently does not adapt to Liquid Glass")
