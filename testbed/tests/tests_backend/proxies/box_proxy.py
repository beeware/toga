from ..page_singleton import BackgroundPage

class BoxProxy:
    """Proxy for toga.Box(children=[...])."""
    def __init__(self, children=None):
        #Create box object remotely
        self.id = self._create_remote_box()
        #If there's children, add them
        if children:
            for child in children:
                self.add(child)

    @classmethod
    def _from_id(cls, box_id: str):
        obj = cls.__new__(cls)
        object.__setattr__(obj, "id", box_id)
        return obj

    def _create_remote_box(self):
        page = BackgroundPage.get()
        code = (
            "new_box = toga.Box()\n"
            "self.my_widgets[new_box.id] = new_box\n"
            "result = new_box.id"
        )
        return page.eval_js("(code) => window.test_cmd(code)", code)

    def add(self, widget):
        page = BackgroundPage.get()
        code = (
            f"self.my_widgets['{self.id}'].add(self.my_widgets['{widget.id}'])"
        )
        page.eval_js("(code) => window.test_cmd(code)", code)