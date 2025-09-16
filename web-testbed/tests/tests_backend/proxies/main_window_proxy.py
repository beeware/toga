from .box_proxy import BoxProxy


class MainWindowProxy:
    # Minimal proxy that can get/set content. Content must be a BoxProxy.

    page_provider = staticmethod(lambda: None)

    def _page(self):
        return type(self).page_provider()

    @property
    def content(self):
        box_id = self._page().eval_js(
            "(code) => window.test_cmd(code)",
            "result = self.main_window.content.id",
        )
        return BoxProxy._from_id(box_id)

    @content.setter
    def content(self, box_proxy):
        self._page().eval_js(
            "(code) => window.test_cmd(code)",
            f"self.main_window.content = self.my_widgets[{repr(box_proxy.id)}]",
        )
