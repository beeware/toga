from .base_proxy import BaseProxy
from .object_proxy import ObjectProxy


class AppProxy(BaseProxy):
    def __init__(self):
        super().__init__("self")


AppProxy.__name__ = AppProxy.__qualname__ = "App"


class BoxProxy(ObjectProxy):
    _ctor_expr = "toga.Box"


BoxProxy.__name__ = BoxProxy.__qualname__ = "Box"


class ButtonProxy(ObjectProxy):
    _ctor_expr = "toga.Button"


ButtonProxy.__name__ = ButtonProxy.__qualname__ = "Button"


class MockProxy(ObjectProxy):
    _ctor_expr = "Mock"


MockProxy.__name__ = MockProxy.__qualname__ = "Mock"
