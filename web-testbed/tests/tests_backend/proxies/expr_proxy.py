class ExprProxy:
    page_provider = staticmethod(lambda: None)

    def __init__(self, ref_expr: str):
        object.__setattr__(self, "_ref_expr", ref_expr)

    def _page(self):
        return type(self).page_provider()

    @property
    def js_ref(self) -> str:
        return object.__getattribute__(self, "_ref_expr")

    def proxy_from_handle(h: dict):
        if h.get("$t") != "handle":
            raise TypeError("not a handle")
        key = h["id"]
        if h.get("ns", "widgets") == "widgets":
            from .widget_proxy import WidgetProxy

            return WidgetProxy.from_id(key)
        else:
            from .non_widget_proxy import NonWidgetProxy

            return NonWidgetProxy.from_id(key)

    def _unwrap(self, v):
        if isinstance(v, dict) and v.get("$t") == "handle":
            return type(self).proxy_from_handle(v)
        # lists/dicts may contain nested handles
        if isinstance(v, list):
            return [self._unwrap(x) for x in v]
        if isinstance(v, dict):
            return {k: self._unwrap(x) for k, x in v.items()}
        return v

    def _encode_value(self, value) -> str:
        from .base_proxy import BaseProxy  # local import to avoid cycle

        if isinstance(value, (ExprProxy, BaseProxy)):
            return value.js_ref
        if isinstance(value, (str, int, float, bool)) or value is None:
            return repr(value)
        if isinstance(value, (list, tuple)):
            inner = ", ".join(self._encode_value(x) for x in value)
            open_, close_ = ("[", "]") if isinstance(value, list) else ("(", ")")
            return f"{open_}{inner}{close_}"
        if isinstance(value, dict):
            items = ", ".join(
                f"{repr(k)}: {self._encode_value(v)}" for k, v in value.items()
            )
            return f"{{{items}}}"
        # raise error if not any of this, will need to implement in the future if needed
        raise TypeError(f"Don't know how to encode {type(value).__name__}. ")

    def _encode_call(self, *args, **kwargs) -> str:
        parts = [self._encode_value(a) for a in args]
        parts += [f"{k}={self._encode_value(v)}" for k, v in kwargs.items()]
        return ", ".join(parts)

    def _is_function(self, name: str) -> bool:
        prop = repr(name)
        code = (
            f"_obj = {self.js_ref}\n"
            f"_attr = getattr(_obj, {prop})\n"
            f"result = callable(_attr)"
        )
        return bool(self._page().eval_js("(code) => window.test_cmd(code)", code))

    def _is_primitive_attr(self, name: str) -> bool:
        prop = repr(name)
        code = (
            f"_obj = {self.js_ref}\n"
            f"_attr = getattr(_obj, {prop})\n"
            "result = isinstance(_attr, (str, int, float, bool)) or _attr is None"
        )
        return bool(self._page().eval_js("(code) => window.test_cmd(code)", code))

    def __getattr__(self, name):
        if self._is_function(name):
            prop = repr(name)

            def _method(*args, **kwargs):
                args_py = self._encode_call(*args, **kwargs)
                code = (
                    f"_obj = {self.js_ref}\n"
                    f"_fn = getattr(_obj, {prop})\n"
                    f"result = _fn({args_py})"
                )
                return self._page().eval_js("(code) => window.test_cmd(code)", code)

            return _method

        if self._is_primitive_attr(name):
            code = f"result = getattr({self.js_ref}, {repr(name)})"
            return self._page().eval_js("(code) => window.test_cmd(code)", code)

        # Return another ExprProxy for attribute objects (ie toga.Button.style)
        return ExprProxy(f"getattr({self.js_ref}, {repr(name)})")

    def __setattr__(self, name, value):
        if name.startswith("_"):
            return object.__setattr__(self, name, value)

        if name == "text":
            rhs = repr(str(value))
        else:
            rhs = self._encode_value(value)
        code = f"setattr({self.js_ref}, {repr(name)}, {rhs})"
        self._page().eval_js("(code) => window.test_cmd(code)", code)

    def __delattr__(self, name):
        if name.startswith("_"):
            return object.__delattr__(self, name)
        code = f"delattr({self.js_ref}, {repr(name)})"
        self._page().eval_js("(code) => window.test_cmd(code)", code)

    def __repr__(self):
        return f"<ExprProxy ref={self.js_ref}>"
