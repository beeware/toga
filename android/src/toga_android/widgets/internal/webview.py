import weakref

from android.webkit import WebResourceRequest, WebView as A_WebView, WebViewClient
from java import Override, jboolean, jvoid, static_proxy
from java.lang import String as jstring


class TogaWebClient(static_proxy(WebViewClient)):
    def __init__(self, impl):
        super().__init__()
        self._webview_impl_ref = weakref.ref(impl)

    @property
    def webview_impl(self):
        return self._webview_impl_ref()

    @Override(jboolean, [A_WebView, WebResourceRequest])
    def shouldOverrideUrlLoading(self, webview, webresourcerequest):
        allow = True
        if self.webview_impl.interface.on_navigation_starting._raw:
            url = webresourcerequest.getUrl().toString()
            result = self.webview_impl.interface.on_navigation_starting(url=url)
            if isinstance(result, bool):
                # on_navigation_starting handler is synchronous
                allow = result
            else:
                # on_navigation_starting handler is asynchronous. Deny navigation until
                # the user defined on_navigation_starting coroutine has completed.
                allow = False
        return not allow

    @Override(jvoid, [A_WebView, jstring])
    def onPageFinished(self, webview, url):
        if self.webview_impl.interface.on_webview_load:
            self.webview_impl.interface.on_webview_load()

        if self.webview_impl.loaded_future:
            self.webview_impl.loaded_future.set_result(None)
            self.webview_impl.loaded_future = None
