from __future__ import annotations

import os
import types
from unittest.mock import Mock

import toga

try:
    import js
except ModuleNotFoundError:
    js = None

try:
    from pyodide.ffi import create_proxy, to_js
except ModuleNotFoundError:
    pyodide = None
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

        self._js_available = (
            js is not None and create_proxy is not None and to_js is not None
        )
        if self._js_available and web_testing_enabled():
            js.window.test_cmd = create_proxy(self.cmd_test)

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
