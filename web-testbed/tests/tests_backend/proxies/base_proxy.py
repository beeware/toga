from .encoding import encode_value


class ProxyProtocolError(RuntimeError):
    # Raised when the remote bridge returns an invalid or unexpected payload.
    pass


class BaseProxy:
    # Remote pure expression proxy
    # Attribute reads auto-realise primitives/containers, everything else stays proxied.

    _storage_expr = "self.my_objs"

    page_provider = staticmethod(lambda: None)

    def __init__(self, js_ref: str):
        self._js_ref = js_ref

    @property
    def js_ref(self) -> str:
        return self._js_ref

    @classmethod
    def _page(cls):
        return cls.page_provider()

    # Core methods

    def __getattr__(self, name: str):
        expr = BaseProxy(f"getattr({self.js_ref}, {repr(name)})")  # attribute handle
        ok, value = self._try_realise_value(expr.js_ref)
        return value if ok else expr

    def __setattr__(self, name: str, value):
        if name.startswith("_"):
            return super().__setattr__(name, value)
        code = f"setattr({self.js_ref}, {repr(name)}, {encode_value(value)})"
        self._eval_and_return(code)

    def __delattr__(self, name: str):
        if name.startswith("_"):
            if hasattr(self, name):
                return super().__delattr__(name)
            raise AttributeError(name)
        code = f"delattr({self.js_ref}, {repr(name)})"
        self._eval_and_return(code)

    def __call__(self, *args, **kwargs):
        parts = []
        if args:
            parts += [encode_value(a) for a in args]
        if kwargs:
            parts += [f"{k}={encode_value(v)}" for k, v in kwargs.items()]
        expr = f"{self.js_ref}({', '.join(parts)})"
        return self._eval_and_return(expr)

    # Resolve/guard
    def resolve(self):
        # Evaluate this expression remotely and return python value
        return self._eval_and_return(self.js_ref)

    def __str__(self):
        v = self.resolve()
        if isinstance(v, str):
            return v
        raise TypeError("Resolved value is not a str; cannot coerce proxy to str.")

    def __int__(self):
        v = self.resolve()
        if isinstance(v, int):
            return v
        raise TypeError("Resolved value is not an int; cannot coerce proxy to int.")

    def __float__(self):
        v = self.resolve()
        if isinstance(v, float):
            return v
        raise TypeError("Resolved value is not a float; cannot coerce proxy to float.")

    def __bool__(self):
        v = self.resolve()
        if isinstance(v, (str, int, float, bool)) or v is None:
            return bool(v)
        if isinstance(v, (list, tuple, dict)):
            return bool(v)
        if isinstance(v, BaseProxy):
            raise TypeError(
                "Truth value of a proxied remote object is ambiguous; "
                "resolve a primitive or compare explicitly."
            )
        raise TypeError(
            "Truth value of a non-primitive remote value is ambiguous; "
            "resolve a primitive or compare explicitly."
        )

    # Remote evaluation
    def _eval_and_return(self, expr_src: str):
        page = self._page()
        payload = page.eval_js(
            "(code) => window.test_cmd(code)", f"result = {expr_src}"
        )
        return self._deserialise_payload(payload)

    def _try_realise_value(self, expr_src: str):
        # Used by __getattr__, try to get a concrete value for primitives/containers.
        # Returns (True, value) for str/int/float/bool/None,
        # list/tuple/dict; else (False, None).
        try:
            val = self._eval_and_return(expr_src)
        except Exception:
            return False, None
        if (
            isinstance(val, (str, int, float, bool))
            or val is None
            or isinstance(val, (list, tuple, dict))
        ):
            return True, val
        return False, None

    def _deserialise_payload(self, payload):
        # De-serialise strict typed envelopes:
        #   - none/bool/int/float/str
        #   - list/tuple/dict (recursive)
        #   - object/callable -> proxy reference (my_objs[id])
        if not isinstance(payload, dict) or "type" not in payload:
            raise ProxyProtocolError(f"Invalid payload from remote: {payload!r}")

        t = payload["type"]

        # primitives
        if t == "none":
            return None
        if t == "bool":
            return bool(payload.get("value"))
        if t == "int":
            return int(payload.get("value"))
        if t == "float":
            return float(payload.get("value"))
        if t == "str":
            return str(payload.get("value"))

        # containers
        if t == "list":
            return [self._deserialise_payload(item) for item in payload.get("items", [])]
        if t == "tuple":
            return tuple(
                self._deserialise_payload(item) for item in payload.get("items", [])
            )
        if t == "dict":
            out = {}
            for k_env, v_env in payload.get("items", []):
                k = self._deserialise_payload(k_env)
                v = self._deserialise_payload(v_env)
                out[k] = v
            return out

        # references
        if t in ("object", "callable"):
            obj_id = payload["id"]
            return BaseProxy(f"{self._storage_expr}[{repr(obj_id)}]")

        raise ProxyProtocolError(f"Unknown payload type: {t!r}")

