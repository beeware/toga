from .object_proxy import ObjectProxy


class MockProxy(ObjectProxy):
    _ctor_expr = "Mock"
