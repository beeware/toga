from .widget_proxy import WidgetProxy


class BoxProxy(WidgetProxy):
    _ctor_expr = "toga.Box"

    def __init__(self, children=None, *args, **kwargs):
        key = self._create_with_known_id(self._ctor_expr, *args, **kwargs)
        super().__init__(key)
        if children:
            for child in children:
                self.add(child)

    @classmethod
    def _from_id(cls, box_id: str):
        obj = cls.__new__(cls)
        WidgetProxy.__init__(obj, box_id)
        return obj

    def add(self, widget):
        child_js = getattr(widget, "js_ref", None)
        if child_js is None:
            child_js = f"{type(self)._storage_expr}[{repr(widget)}]"
        self._page().eval_js(
            "(code) => window.test_cmd(code)",
            f"{self.js_ref}.add({child_js})",
        )
