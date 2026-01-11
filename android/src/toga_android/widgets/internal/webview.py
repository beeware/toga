import weakref

from android.webkit import WebResourceRequest, WebView as A_WebView, WebViewClient
from java import Override, jboolean, jvoid, static_proxy
from java.lang import String as jstring


class TogaWebClient(static_proxy(WebViewClient)):
    def __init__(self, impl):
        self.impl = weakref.proxy(impl)
        self.interface = weakref.proxy(impl.interface)
        super().__init__()

    @Override(jboolean, [A_WebView, WebResourceRequest])
    def shouldOverrideUrlLoading(self, webview, webresourcerequest):
        allow = True
        try:
            if self.interface.on_navigation_starting._raw:
                url = webresourcerequest.getUrl().toString()
                result = self.interface.on_navigation_starting(url=url)
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

    @Override(jvoid, [A_WebView, jstring])
    def onPageFinished(self, webview, url):
        try:
            self.interface.on_webview_load()
        # It's possible for this handler to be invoked *after* the interface/impl object
        # has been destroyed. If the interface/impl doesn't exist there's no handler to
        # invoke either, so ignore the edge case. This can't be reproduced reliably, so
        # it is no-covered.
        except ReferenceError:  # pragma: no cover
            pass

        try:
            if self.impl.loaded_future:
                self.impl.loaded_future.set_result(None)
                self.impl.loaded_future = None
        except ReferenceError:  # pragma: no cover
            pass
