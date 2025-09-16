from .non_widget_proxy import NonWidgetProxy


class MockProxy(NonWidgetProxy):
    _ctor_expr = "Mock"

    def __init__(self, *args, **kwargs):
        key = self._create(self._ctor_expr, *args, **kwargs)
        super().__init__(key)
