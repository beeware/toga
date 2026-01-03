import weakref

from android.webkit import WebResourceRequest, WebView as A_WebView, WebViewClient
from java import Override, jboolean, static_proxy


class TogaWebClient(static_proxy(WebViewClient)):
    def __init__(self, impl):
        super().__init__()
        self.webview_impl = weakref.proxy(impl)

    @Override(jboolean, [A_WebView, WebResourceRequest])
    def shouldOverrideUrlLoading(self, webview, webresourcerequest):
        allow = True
        try:
            if self.webview_impl.interface.on_navigation_starting._raw:
                url = webresourcerequest.getUrl().toString()
                result = self.webview_impl.interface.on_navigation_starting(url=url)
                if isinstance(result, bool):
                    # on_navigation_starting handler is synchronous
                    allow = result
                else:
                    # on_navigation_starting handler is asynchronous. Deny navigation
                    # until the user defined on_navigation_starting coroutine has
                    # completed.
                    allow = False
        # This is a defensive safety catch, just in case if the impl object
        # has already been collected, but the native widget is still
        # emitting an event to the listener.
        except ReferenceError:  # pragma: no cover
            pass
        return not allow
