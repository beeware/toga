from android.webkit import WebResourceRequest, WebView as A_WebView, WebViewClient
from java import Override, jboolean, static_proxy


class TogaWebClient(static_proxy(WebViewClient)):
    def __init__(self, impl):
        super().__init__()
        self.webview_impl = impl

    @Override(jboolean, [A_WebView, WebResourceRequest])
    def shouldOverrideUrlLoading(self, webview, webresourcerequest):
        if self.webview_impl.interface.on_navigation_starting:
            allow = self.webview_impl.interface.on_navigation_starting(
                url=webresourcerequest.getUrl().toString()
            )
            if not allow:
                return True
        return False


# TogaWebClient
