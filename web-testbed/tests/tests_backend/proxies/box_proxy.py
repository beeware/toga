class BoxProxy:
    """Proxy for toga.Box(children=[...])."""

    page_provider = staticmethod(lambda: None)

    def _page(self):
        return type(self).page_provider()

    def __init__(self, children=None):
        # Create box object remotely
        self.id = self._create_remote_box()
        # If there's children, add them
        if children:
            for child in children:
                self.add(child)

    @classmethod
    def _from_id(cls, box_id: str):
        obj = cls.__new__(cls)
        object.__setattr__(obj, "id", box_id)
        return obj

    def _create_remote_box(self):
        code = (
            "new_box = toga.Box()\n"
            "self.my_widgets[new_box.id] = new_box\n"
            "result = new_box.id"
        )
        return self._page().eval_js("(code) => window.test_cmd(code)", code)

    def add(self, widget):
        code = f"self.my_widgets['{self.id}'].add(self.my_widgets['{widget.id}'])"
        self._page().eval_js("(code) => window.test_cmd(code)", code)
