from toga_cocoa.libs import WKWebView

from .base import SimpleProbe


class WebViewProbe(SimpleProbe):
    native_class = WKWebView

    async def get_page_content(self):
        return await self.impl.evaluate_javascript("document.body.innerHTML")
