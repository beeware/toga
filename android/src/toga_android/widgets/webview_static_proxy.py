import weakref

from android.webkit import WebResourceRequest, WebView as A_WebView, WebViewClient
from java import Override, jboolean, static_proxy


class TogaWebClient(static_proxy(WebViewClient)):
    def __init__(self, impl):
        super().__init__()
        self._webview_impl_ref = weakref.ref(impl)

    @property
    def webview_impl(self):
        return self._webview_impl_ref()

    @Override(jboolean, [A_WebView, WebResourceRequest])
    def shouldOverrideUrlLoading(self, webview, webresourcerequest):
        if self.webview_impl.interface.on_navigation_starting:
            url = webresourcerequest.getUrl().toString()
            result = self.webview_impl.interface.on_navigation_starting(url=url)
            if isinstance(result, bool):
                # on_navigation_starting handler is synchronous
                allow = result
            else:
                # on_navigation_starting handler is asynchronous
                # deny the navigation until the user himself or the user
                # defined on_navigation_starting handler has allowed it
                allow = False
            if not allow:
                return True
        return False
