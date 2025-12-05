import asyncio

from android.webkit import WebResourceRequest, WebView as A_WebView, WebViewClient
from java import Override, jboolean, static_proxy


class TogaWebClient(static_proxy(WebViewClient)):
    def __init__(self, impl):
        super().__init__()
        self.webview_impl = impl

    @Override(jboolean, [A_WebView, WebResourceRequest])
    def shouldOverrideUrlLoading(self, webview, webresourcerequest):
        if self.webview_impl.interface.on_navigation_starting:
            url = webresourcerequest.getUrl().toString()
            # check URL permission
            if (
                self.webview_impl.interface._url_allowed == "about:blank"
                or self.webview_impl.interface._url_allowed == url
            ):
                # URL is allowed by user code
                allow = True
            else:
                # allow the URL only once
                self.webview_impl.interface._url_allowed = None
                result = self.webview_impl.interface.on_navigation_starting(url=url)
                if isinstance(result, bool):
                    # on_navigation_starting handler is synchronous
                    allow = result
                elif isinstance(result, asyncio.Future):
                    # on_navigation_starting handler is asynchronous
                    if result.done():
                        allow = result.result()
                    else:
                        # deny the navigation until the user himself or the user
                        # defined on_navigation_starting handler has allowed it
                        allow = False
            if not allow:
                return True
        return False
