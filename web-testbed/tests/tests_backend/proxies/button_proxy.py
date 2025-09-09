from .base_proxy import BaseProxy


class ButtonProxy(BaseProxy):
    def __init__(self, text="Hello"):
        code = (
            f"new_widget = toga.Button({repr(text)})\n"
            "self.my_widgets[new_widget.id] = new_widget\n"
            "result = new_widget.id"
        )
        wid = self._page().eval_js("(code) => window.test_cmd(code)", code)
        super().__init__(wid)
