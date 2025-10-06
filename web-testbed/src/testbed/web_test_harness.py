from __future__ import annotations

import datetime as _dt
import os
import textwrap
import types
from unittest.mock import Mock

import toga

try:
    import js
except ModuleNotFoundError:
    js = None

try:
    from pyodide.ffi import create_proxy, to_js
except Exception:
    create_proxy = None
    to_js = None


def _truthy(v) -> bool:
    return str(v).strip().lower() in {"1", "true", "yes", "on"}


def web_testing_enabled() -> bool:
    if _truthy(os.getenv("TOGA_WEB_TESTING")):
        return True

    if js is not None:
        try:
            if _truthy(getattr(js.window, "TOGA_WEB_TESTING", "")):
                return True
            qs = str(getattr(js.window, "location", None).search or "")
            if "toga_web_testing" in qs.lower():
                return True
        except Exception:
            pass
    return False


class WebTestHarness:
    def __init__(self, app, *, expose_name: str = "test_cmd"):
        self.app = app
        self.my_objs = {}
        self.app.my_objs = self.my_objs
        self._capabilities = {}
        self.my_objs["__caps__"] = self._capabilities

        self.my_objs["__app__"] = self.app

        self._js_available = (
            js is not None and create_proxy is not None and to_js is not None
        )
        if self._js_available and web_testing_enabled():
            js.window.test_cmd = create_proxy(self.cmd_test)
            js.window.test_cmd_rpc = create_proxy(self.cmd_test_rpc)

    def cmd_test(self, code):
        try:
            env = globals().copy()
            env.update(locals())

            env["self"] = self.app
            env["toga"] = toga
            env["my_objs"] = self.my_objs
            env["Mock"] = Mock

            exec(code, env, env)
            result = env.get("result")
            envelope = self._serialise_payload(result)
            return to_js(envelope, dict_converter=js.Object.fromEntries)
        except Exception as e:
            return to_js(
                {"type": "error", "value": str(e)}, dict_converter=js.Object.fromEntries
            )

    def _serialise_payload(self, x):
        # primitives
        if x is None:
            return {"type": "none", "value": None}
        if isinstance(x, bool):
            return {"type": "bool", "value": x}
        if isinstance(x, int):
            return {"type": "int", "value": x}
        if isinstance(x, float):
            return {"type": "float", "value": x}
        if isinstance(x, str):
            return {"type": "str", "value": x}

        # containers
        if isinstance(x, list):
            return {"type": "list", "items": [self._serialise_payload(i) for i in x]}
        if isinstance(x, tuple):
            return {"type": "tuple", "items": [self._serialise_payload(i) for i in x]}
        if isinstance(x, dict):
            items = []
            for k, v in x.items():
                if k is None:
                    key_env = {"type": "none", "value": None}
                elif isinstance(k, bool):
                    key_env = {"type": "bool", "value": k}
                elif isinstance(k, int):
                    key_env = {"type": "int", "value": k}
                elif isinstance(k, float):
                    key_env = {"type": "float", "value": k}
                elif isinstance(k, str):
                    key_env = {"type": "str", "value": k}
                else:
                    key_env = {"type": "str", "value": str(k)}
                items.append([key_env, self._serialise_payload(v)])
            return {"type": "dict", "items": items}
        if isinstance(x, _dt.time):
            return {"type": "time", "value": x.strftime("%H:%M:%S")}
        if isinstance(x, _dt.date) and not isinstance(x, _dt.datetime):
            return {"type": "date", "value": x.strftime("%m/%d/%Y")}

        # references by id
        obj_id = self._key_for(x)
        is_callable = callable(x) or isinstance(
            x, (types.FunctionType, types.MethodType)
        )
        return {"type": "callable" if is_callable else "object", "id": obj_id}

    def _key_for(self, x):
        for k, v in self.my_objs.items():
            if v is x:
                return k
        # If not registered, register it
        k = str(id(x))
        self.my_objs[k] = x
        return k

    def _deserialise(self, env):
        if env is None:
            return None
        if not isinstance(env, dict):
            return env

        t = env.get("type")
        if t in (None, "none"):
            return None
        if t == "bool":
            return bool(env["value"])
        if t == "int":
            return int(env["value"])
        if t == "float":
            return float(env["value"])
        if t == "str":
            return str(env["value"])
        if t == "list":
            return [self._deserialise(i) for i in env["items"]]
        if t == "tuple":
            return tuple(self._deserialise(i) for i in env["items"])
        if t == "dict":
            out = {}
            for k_env, v_env in env["items"]:
                k = self._deserialise(k_env)
                v = self._deserialise(v_env)
                out[k] = v
            return out
        if t == "time":
            s = env["value"]
            h, m, *rest = s.split(":")
            sec = int(rest[0]) if rest else 0
            return _dt.time(int(h), int(m), sec)
        if t == "date":
            s = env["value"]
            try:
                return _dt.datetime.strptime(s, "%m/%d/%Y").date()
            except ValueError:
                return _dt.date.fromisoformat(s)
        # reconstruct functions from source
        if t == "callable_source":
            try:
                scope = {}
                exec(textwrap.dedent(env["source"]), scope, scope)
                fn = scope.get(env["name"])
            except Exception as e:
                raise ValueError(
                    f"Failed to exec callable source for {env.get('name')!r}"
                ) from e

            if not callable(fn):
                raise ValueError(
                    f"Callable {env.get('name')!r} not found or not callable after exec"
                )
            return fn
        if t in ("ref", "object"):
            ref = env.get("ref")
            if ref is None:
                ref = env.get("id")
            return self.my_objs[str(ref)]
        return env

    def cmd_test_rpc(self, msg):
        m = msg.to_py() if hasattr(msg, "to_py") else msg

        op = m["op"]

        if op == "getattr":
            obj = self.my_objs[str(m["obj"])]
            value = getattr(obj, m["name"])
            return to_js(
                self._serialise_payload(value), dict_converter=js.Object.fromEntries
            )

        if op == "setattr":
            obj = self.my_objs[str(m["obj"])]
            setattr(obj, m["name"], self._deserialise(m["value"]))
            return to_js(
                self._serialise_payload(None), dict_converter=js.Object.fromEntries
            )

        if op == "delattr":
            obj = self.my_objs[str(m["obj"])]
            delattr(obj, m["name"])
            return to_js(
                self._serialise_payload(None), dict_converter=js.Object.fromEntries
            )

        if op == "call":
            fn = self.my_objs[str(m["fn"])]
            args = [self._deserialise(a) for a in m.get("args", [])]
            kwargs = {k: self._deserialise(v) for k, v in m.get("kwargs", {}).items()}
            out = fn(*args, **kwargs)
            return to_js(
                self._serialise_payload(out), dict_converter=js.Object.fromEntries
            )

        if op == "hostcall":
            fn = self._capabilities.get(m["name"])
            if not fn:
                return to_js(
                    {"type": "error", "value": f"Unknown capability: {m['name']}"},
                    dict_converter=js.Object.fromEntries,
                )
            try:
                out = fn(
                    *[self._deserialise(a) for a in m.get("args", [])],
                    **{k: self._deserialise(v) for k, v in m.get("kwargs", {}).items()},
                )
                env = self._serialise_payload(out)
            except Exception as e:
                env = {"type": "error", "value": f"{type(e).__name__}: {e}"}
            return to_js(env, dict_converter=js.Object.fromEntries)

        # Potential use for future, instead of '_create'
        if op == "new":
            ctor = m["ctor"]
            args = [self._deserialise(a) for a in m.get("args", [])]
            kwargs = {k: self._deserialise(v) for k, v in m.get("kwargs", {}).items()}
            module_name, _, name = ctor.rpartition(".")
            mod = __import__(module_name, fromlist=[name]) if module_name else globals()
            cls = getattr(mod, name) if module_name else globals()[name]
            obj = cls(*args, **kwargs)
            key = self._key_for(obj)
            return to_js(
                self._serialise_payload(key), dict_converter=js.Object.fromEntries
            )

        raise ValueError(f"Unknown op {op!r}")
