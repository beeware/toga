from .base import ProxyBase


class ButtonProxy(ProxyBase):
    def __init__(self):
        object.__setattr__(self, "_inited", False)

        code = (
            "new_widget = toga.Button('Hello')\n"
            "self.my_widgets[new_widget.id] = new_widget\n"
            "result = new_widget.id"
        )
        widget_id = self._page().eval_js("(code) => window.test_cmd(code)", code)

        object.__setattr__(self, "id", widget_id)
        object.__setattr__(self, "_inited", True)
