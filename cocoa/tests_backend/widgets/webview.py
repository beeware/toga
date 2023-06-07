from toga_cocoa.libs import WKWebView

from .base import SimpleProbe


class WebViewProbe(SimpleProbe):
    native_class = WKWebView
    content_supports_url = True
    javascript_supports_exception = True

    async def get_page_content(self):
        return await self.impl.evaluate_javascript("document.body.innerHTML")
