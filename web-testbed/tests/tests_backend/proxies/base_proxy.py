import datetime as _dt
import inspect


class ProxyProtocolError(RuntimeError):
    # Raised when the remote bridge returns an invalid or unexpected payload.
    pass


class BaseProxy:
    # Remote pure expression proxy
    # Attribute reads auto-realise primitives/containers, everything else stays proxied.

    _storage_expr = "self.my_objs"

    page_provider = staticmethod(lambda: None)

    # cache: js_ref to proxy instance
    _instances = {}

    # per-class default local names
    _local_whitelist = frozenset()

    def __init__(self, js_ref: str):
        self._js_ref = js_ref
        self._local_attrs = {}
        self._local_names = set()
        BaseProxy._instances[js_ref] = self

    @property
    def js_ref(self) -> str:
        return self._js_ref

    @classmethod
    def _page(cls):
        return cls.page_provider()

    # Core methods

    def __getattr__(self, name: str):
        if self._is_declared_local(name):
            local = self._local_attrs
            if name in local:
                return local[name]
        return self._rpc("getattr", obj=self._ref(), name=name)

    def __setattr__(self, name: str, value):
        if name.startswith("_"):
            return super().__setattr__(name, value)

        # respect data descriptors (e.g., @property setter)
        cls_attr = getattr(type(self), name, None)
        if hasattr(cls_attr, "__set__"):
            return object.__setattr__(self, name, value)

        # keep local policy intact
        if self._is_declared_local(name):
            self._local_attrs[name] = value
            return

        # RPC setattr
        try:
            env = self._serialise_for_rpc(value, self._storage_expr)
        except Exception:
            # if something truly can't be serialized, keep it local.
            self._local_attrs[name] = value
            return
        self._rpc("setattr", obj=self._ref(), name=name, value=env)
        self._local_attrs.clear()

    def __delattr__(self, name: str):
        if name.startswith("_"):
            if hasattr(self, name):
                return super().__delattr__(name)
            raise AttributeError(name)

        local = self._local_attrs
        if name in local:
            del local[name]
            return

        self._rpc("delattr", obj=self._ref(), name=name)
        self._local_attrs.clear()

    def __call__(self, *args, **kwargs):
        args_env = [self._serialise_for_rpc(a, self._storage_expr) for a in args]
        kwargs_env = {
            k: self._serialise_for_rpc(v, self._storage_expr) for k, v in kwargs.items()
        }
        return self._rpc("call", fn=self._ref(), args=args_env, kwargs=kwargs_env)

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
            return [
                self._deserialise_payload(item) for item in payload.get("items", [])
            ]
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

        if t == "time":
            s = payload.get("value", "")
            parts = [int(p) for p in s.split(":")]
            if len(parts) == 2:
                h, m = parts
                sec = 0
            else:
                h, m, sec = (parts + [0, 0, 0])[:3]
            return _dt.time(h, m, sec)

        if t == "date":
            s = payload.get("value", "")
            try:
                return _dt.datetime.strptime(s, "%m/%d/%Y").date()
            except ValueError:
                return _dt.date.fromisoformat(s)

        # references
        if t in ("object", "callable"):
            obj_id = payload["id"]
            js_ref = f"{self._storage_expr}[{repr(obj_id)}]"
            existing = BaseProxy._instances.get(js_ref)
            if existing is not None:
                return existing
            p = BaseProxy(js_ref)
            # cache the parsed id to avoid re-parsing js_ref later
            p.__dict__["_ref_cache"] = str(obj_id)
            return p

        if t == "error":
            raise ProxyProtocolError(payload.get("value"))

        raise ProxyProtocolError(f"Unknown payload type: {t!r}")

    # local policy - keep Python-only stuff local
    # private names, explicitly declared names, and any value containing Python
    # callables stay in _local_attrs
    # only primitives/containers and remote proxies are forwarded.
    def _is_declared_local(self, name: str) -> bool:
        return (
            name in object.__getattribute__(self, "_local_names")
            or name in type(self)._local_whitelist
        )

    @staticmethod
    def _extract_ref_from_expr(expr: str, storage_expr: str = "self.my_objs") -> str:
        prefix = f"{storage_expr}["
        if expr.startswith(prefix) and expr.endswith("]"):
            inner = expr[len(prefix) : -1].strip()
            if (inner.startswith("'") and inner.endswith("'")) or (
                inner.startswith('"') and inner.endswith('"')
            ):
                inner = inner[1:-1]
            return inner
        return expr  # fallback

    def _serialise_for_rpc(self, v, storage_expr="self.my_objs"):
        # proxies first (no getattr!)
        if isinstance(v, BaseProxy):
            return {"type": "ref", "id": v._ref()}
        if hasattr(v, "js_ref"):  # duck-typed proxy
            return {
                "type": "ref",
                "id": self._extract_ref_from_expr(v.js_ref, storage_expr),
            }
        # primitives
        if v is None:
            return {"type": "none", "value": None}
        if isinstance(v, bool):
            return {"type": "bool", "value": v}
        if isinstance(v, int):
            return {"type": "int", "value": v}
        if isinstance(v, float):
            return {"type": "float", "value": v}
        if isinstance(v, str):
            return {"type": "str", "value": v}
        # containers
        if isinstance(v, list):
            return {
                "type": "list",
                "items": [self._serialise_for_rpc(i, storage_expr) for i in v],
            }
        if isinstance(v, tuple):
            return {
                "type": "tuple",
                "items": [self._serialise_for_rpc(i, storage_expr) for i in v],
            }
        if isinstance(v, dict):
            items = []
            for k, val in v.items():
                if k is None:
                    k_env = {"type": "none", "value": None}
                elif isinstance(k, bool):
                    k_env = {"type": "bool", "value": k}
                elif isinstance(k, int):
                    k_env = {"type": "int", "value": k}
                elif isinstance(k, float):
                    k_env = {"type": "float", "value": k}
                elif isinstance(k, str):
                    k_env = {"type": "str", "value": k}
                else:
                    k_env = {"type": "str", "value": str(k)}
                items.append([k_env, self._serialise_for_rpc(val, storage_expr)])
            return {"type": "dict", "items": items}

        if isinstance(v, _dt.time):
            # use “HH:MM:SS”
            return {"type": "time", "value": v.strftime("%H:%M:%S")}

        if isinstance(v, _dt.date) and not isinstance(v, _dt.datetime):
            # use “YYYY/MM/DD”
            return {"type": "date", "value": v.strftime("%m/%d/%Y")}

        if callable(v):
            src = inspect.getsource(v)
            name = getattr(v, "__name__", None) or "anonymous"
            return {
                "type": "callable_source",
                "name": name,
                "source": src,
            }

        # final fallback: encoding unknowns as text
        return {"type": "str", "value": str(v)}

    def _ref(self) -> str:
        r = self.__dict__.get("_ref_cache")
        if r is None:
            r = self._extract_ref_from_expr(self.js_ref, self._storage_expr)
            self.__dict__["_ref_cache"] = r
        return r

    def _rpc(self, op, **kwargs):
        page = self._page()
        payload = page.eval_js(
            "(msg) => window.test_cmd_rpc(msg)", {"op": op, **kwargs}
        )
        return self._deserialise_payload(payload)

    @classmethod
    def call_host(cls, name: str, *args, **kwargs):
        temp = cls("self.my_objs['__app__']")

        args_env = [temp._serialise_for_rpc(a, temp._storage_expr) for a in args]
        kwargs_env = {
            k: temp._serialise_for_rpc(v, temp._storage_expr) for k, v in kwargs.items()
        }

        page = cls._page()
        payload = page.eval_js(
            "(m) => window.test_cmd_rpc(m)",
            {"op": "hostcall", "name": name, "args": args_env, "kwargs": kwargs_env},
        )
        return temp._deserialise_payload(payload)
