import weakref

from android.webkit import (
    WebResourceRequest,
    WebResourceResponse,
    WebView as A_WebView,
    WebViewClient,
)
from androidx.webkit import WebViewAssetLoader
from java import Override, dynamic_proxy, jboolean, jvoid, static_proxy
from java.io import FileInputStream
from java.lang import String as jstring

import toga


class TogaCachePathHandler(dynamic_proxy(WebViewAssetLoader.PathHandler)):
    def __init__(self, impl):
        super().__init__()
        self.impl = impl

    @Override(WebResourceResponse, [jstring])
    def handle(self, path):
        filepath = toga.App.app.paths.cache / path
        if filepath.exists():
            return WebResourceResponse(
                "text/html", "utf-8", FileInputStream(str(filepath))
            )
        return None


class TogaWebClient(static_proxy(WebViewClient)):
    def __init__(self, impl):
        self._interface_ref = weakref.ref(impl.interface)
        self._impl_ref = weakref.ref(impl)
        pathHandler = TogaCachePathHandler(impl._native_activity)
        self.cache_assetLoader = (
            WebViewAssetLoader.Builder().addPathHandler("/cache/", pathHandler).build()
        )
        super().__init__()

    @property
    def interface(self):
        return self._interface_ref()

    @property
    def impl(self):
        return self._impl_ref()

    @Override(jboolean, [A_WebView, WebResourceRequest])
    def shouldOverrideUrlLoading(self, webview, webresourcerequest):
        allow = True
        if self.interface and self.interface.on_navigation_starting._raw:
            url = webresourcerequest.getUrl().toString()
            result = self.interface.on_navigation_starting(url=url)
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
        # It's possible for this handler to be invoked *after* the interface/impl object
        # has been destroyed. If the interface/impl doesn't exist there's no handler to
        # invoke either, so ignore the edge case. This can't be reproduced reliably, so
        # don't check coverage on the `is None` case.
        if self.interface:  # pragma: no-branch
            self.interface.on_webview_load()

        if self.impl and self.impl.loaded_future:  # pragma: no-branch
            self.impl.loaded_future.set_result(None)
            self.impl.loaded_future = None

    @Override(WebResourceResponse, [A_WebView, WebResourceRequest])
    def shouldInterceptRequest(self, webview, request):
        return self.cache_assetLoader.shouldInterceptRequest(request.getUrl())
