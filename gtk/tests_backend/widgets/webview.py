from toga_gtk.libs import WebKit2

from .base import SimpleProbe


class WebViewProbe(SimpleProbe):
    native_class = WebKit2.WebView

    async def get_page_content(self):
        return await self.impl.evaluate_javascript("document.body.innerHTML")
