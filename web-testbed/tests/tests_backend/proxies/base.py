class ProxyBase:
    page_provider = staticmethod(lambda: None)

    def _page(self):
        return type(self).page_provider()

    # Extend to also hold other objects, including app and main_window?
    def __str__(self):
        widget_id = object.__getattribute__(self, "id")
        return f"self.my_widgets[{widget_id!r}]"

    def __setattr__(self, name, value):
        # METHOD 1 (working)
        literal = (
            repr(str(value))
            if not isinstance(value, (int, float, bool, type(None)))
            else repr(value)
        )

        # METHOD 2 (working)
        # try:
        # literal = json.dumps(value)
        # except TypeError:
        # literal = json.dumps(str(value))

        # METHOD 3 (working)
        # if name == "text":
        # literal = repr(str(value))
        # else:
        # try:
        # literal = json.dumps(value)
        # except TypeError:
        # literal = repr(value)

        code = f"{str(self)}.{name} = {literal}"
        self._page().eval_js("(code) => window.test_cmd(code)", code)

    def __getattr__(self, name):
        code = f"result = {str(self)}.{name}"

        return self._page().eval_js("(code) => window.test_cmd(code)", code)
