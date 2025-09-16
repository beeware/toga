from .expr_proxy import ExprProxy


class BaseProxy(ExprProxy):
    _storage_expr: str = "self.my_widgets"

    page_provider = staticmethod(lambda: None)

    def _page(self):
        return type(self).page_provider()

    def __init__(self, object_key: str):
        object.__setattr__(self, "_id", object_key)
        ref_expr = f"{type(self)._storage_expr}[{repr(object_key)}]"
        super().__init__(ref_expr)

    @property
    def id(self) -> str:
        return object.__getattribute__(self, "_id")

    @classmethod
    def from_id(cls, object_key: str):
        self = object.__new__(cls)
        BaseProxy.__init__(self, object_key)
        return self

    def __repr__(self):
        return f"<{type(self).__name__} id={self.id}>"
