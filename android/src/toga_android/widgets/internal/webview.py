import weakref

from android.webkit import (
    WebResourceRequest,
    WebResourceResponse,
    WebView as A_WebView,
    WebViewClient,
)
from java import Override, dynamic_proxy, jboolean, jvoid, static_proxy
from java.io import FileInputStream
from java.lang import String as jstring

import toga

from ..base import suppress_reference_error

try:
    from androidx.webkit import WebViewAssetLoader
except ImportError:  # pragma: no cover
    WebViewAssetLoader = None


class TogaWebClient(static_proxy(WebViewClient)):
    def __init__(self, impl):
        self.impl = weakref.proxy(impl)
        self.interface = weakref.proxy(impl.interface)
        if WebViewAssetLoader is not None:
            pathHandler = TogaCachePathHandler(self)
            self.cache_assetLoader = (
                WebViewAssetLoader.Builder()
                .addPathHandler("/cache/", pathHandler)
                .build()
            )
        else:  # pragma: no cover
            self.cache_assetLoader = None
        super().__init__()

    @Override(jboolean, [A_WebView, WebResourceRequest])
    def shouldOverrideUrlLoading(self, webview, webresourcerequest):
        allow = True
        with suppress_reference_error():
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
        return not allow

    @Override(jvoid, [A_WebView, jstring])
    def onPageFinished(self, webview, url):
        with suppress_reference_error():
            self.interface.on_webview_load()
            if self.impl.loaded_future:
                self.impl.loaded_future.set_result(None)
                self.impl.loaded_future = None

    @Override(WebResourceResponse, [A_WebView, WebResourceRequest])
    # This method is called in a separate thread and therefore not recognized
    # by the coverage test
    def shouldInterceptRequest(self, webview, request):  # pragma no cover
        if self.cache_assetLoader:
            return self.cache_assetLoader.shouldInterceptRequest(request.getUrl())


class TogaCachePathHandler(dynamic_proxy(WebViewAssetLoader.PathHandler)):
    def __init__(self, webclient):
        super().__init__()
        self.webclient = webclient

    @Override(WebResourceResponse, [jstring])
    # This method is called in a separate thread and therefore not recognized
    # by the coverage test
    def handle(self, path):  # pragma no cover
        filepath = toga.App.app.paths.cache / path
        if filepath.exists():
            return WebResourceResponse(
                "text/html", "utf-8", FileInputStream(str(filepath))
            )
        return None
