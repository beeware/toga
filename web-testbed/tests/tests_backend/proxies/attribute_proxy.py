from .expr_proxy import ExprProxy


class AttributeProxy(ExprProxy):
    def __init__(self, owner: ExprProxy, name: str):
        ref_expr = f"getattr({owner.js_ref}, {repr(name)})"
        super().__init__(ref_expr)
