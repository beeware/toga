from .base_proxy import BaseProxy


class WidgetProxy(BaseProxy):
    # In-built widget register
    # Using my_widgets for all objects for now
    # _storage_expr = "self.widgets"

    def _create_with_known_id(self, ctor_expr: str, *args, **kwargs) -> str:
        call_args = self._encode_call(*args, **kwargs)
        code = (
            f"new_widget = {ctor_expr}({call_args})\n"
            "self.my_widgets[new_widget.id] = new_widget\n"
            "result = new_widget.id"
        )
        return self._page().eval_js("(code) => window.test_cmd(code)", code)

    def add_to_main_window(self):
        self._page().eval_js(
            "(code) => window.test_cmd(code)",
            f"self.main_window.content.add({self.js_ref})",
        )
