from ..page_singleton import BackgroundPage
import json

class ButtonProxy:
    def __init__(self):
        object.__setattr__(self, "_inited", False)

        button_id = self.setup()
        object.__setattr__(self, "id", button_id)

        object.__setattr__(self, "_inited", True)
    
    def __setattr__(self, name, value):
        page = BackgroundPage.get()
        widget_id = object.__getattribute__(self, "id")

        # METHOD 1 (working)
        
        literal = repr(str(value)) if not isinstance(value, (int, float, bool, type(None))) else repr(value)
        
        # METHOD 2 (working)
        """
        try:
            literal = json.dumps(value)
        except TypeError:
            literal = json.dumps(str(value))
        """
        # METHOD 3 (working)
        """
        if name == "text":
            literal = repr(str(value))
        else:
            try:
                literal = json.dumps(value)
            except TypeError:
                literal = repr(value)
        """

        code = f"self.my_widgets[{widget_id!r}].{name} = {literal}"
        page.eval_js("(code) => window.test_cmd(code)", code)

    def __getattr__(self, name):
        page = BackgroundPage.get()

        code = (
            f"result = self.my_widgets['{self.id}'].{name}"
        )

        return page.eval_js("(code) => window.test_cmd(code)", code)

    def setup(self):
        page = BackgroundPage.get()
        code = (
            "new_widget = toga.Button('Hello')\n"
            "self.my_widgets[new_widget.id] = new_widget\n"
            "result = new_widget.id"
        )
        return page.eval_js("(code) => window.test_cmd(code)", code)


