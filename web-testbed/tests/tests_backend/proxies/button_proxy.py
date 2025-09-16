from .widget_proxy import WidgetProxy


class ButtonProxy(WidgetProxy):
    _ctor_expr = "toga.Button"

    def __init__(self, *args, **kwargs):
        key = self._create_with_known_id(self._ctor_expr, *args, **kwargs)
        super().__init__(key)
