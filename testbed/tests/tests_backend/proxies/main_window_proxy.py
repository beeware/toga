from ..page_singleton import BackgroundPage
from .box_proxy import BoxProxy

class MainWindowProxy:
    """Proxy that can get/set content. Content must be a BoxProxy."""

    @property
    def content(self):
        page = BackgroundPage.get()
        code = "result = self.main_window.content.id"
        box_id = page.eval_js("(code) => window.test_cmd(code)", code)
        if box_id is None:
            return BoxProxy()
        proxy = BoxProxy.__new__(BoxProxy)
        proxy.id = box_id
        return proxy

    @content.setter
    def content(self, box_proxy):
        page = BackgroundPage.get()
        code = f"self.main_window.content = self.my_widgets['{box_proxy.id}']"
        page.eval_js("(code) => window.test_cmd(code)", code)
