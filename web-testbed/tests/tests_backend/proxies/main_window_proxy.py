from .box_proxy import BoxProxy


class MainWindowProxy:
    """Minimal proxy that can get/set content. Content must be a BoxProxy."""

    page_provider = staticmethod(lambda: None)

    def _page(self):
        return type(self).page_provider()

    @property
    def content(self):
        code = "result = self.main_window.content.id"
        box_id = self._page().eval_js("(code) => window.test_cmd(code)", code)
        if box_id is None:
            return BoxProxy()
        proxy = BoxProxy.__new__(BoxProxy)
        proxy.id = box_id
        return proxy

    @content.setter
    def content(self, box_proxy):
        code = f"self.main_window.content = self.my_widgets['{box_proxy.id}']"
        self._page().eval_js("(code) => window.test_cmd(code)", code)
