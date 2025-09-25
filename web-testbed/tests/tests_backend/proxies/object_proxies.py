from .object_proxy import ObjectProxy


class BoxProxy(ObjectProxy):
    _ctor_expr = "toga.Box"


class ButtonProxy(ObjectProxy):
    _ctor_expr = "toga.Button"


class MockProxy(ObjectProxy):
    _ctor_expr = "Mock"
