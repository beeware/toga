from .object_proxy import ObjectProxy


class BoxProxy(ObjectProxy):
    _ctor_expr = "toga.Box"

    def __init__(self, children=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if children:
            for child in children:
                self.add(child)
