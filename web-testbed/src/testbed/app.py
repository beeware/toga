import os
import types
from unittest.mock import Mock

import toga
from toga.style import Pack
from toga.style.pack import COLUMN

try:
    import js
except ModuleNotFoundError:
    js = None
try:
    from pyodide.ffi import create_proxy, to_js
except ModuleNotFoundError:
    pyodide = None


def _truthy(v) -> bool:
    return str(v).strip().lower() in {"1", "true", "yes", "on"}


def _web_testing_enabled() -> bool:
    if _truthy(os.getenv("TOGA_WEB_TESTING")):
        return True

    if js is not None:
        try:
            if _truthy(getattr(js.window, "TOGA_WEB_TESTING", "")):
                return True
            qs = str(getattr(js.window, "location", None).search or "")
            # enable if ?toga_web_testing=1 in url
            if "toga_web_testing" in qs.lower():
                return True
        except Exception:
            pass

    return False


class HelloWorld(toga.App):
    def startup(self):
        main_box = toga.Box(style=Pack(direction=COLUMN))
        self.label = toga.Label(id="myLabel", text="Test App - Toga Web Testing")

        if _web_testing_enabled() and js is not None and create_proxy is not None:
            self.my_objs = {}
            js.window.test_cmd = create_proxy(self.cmd_test)

        main_box.add(self.label)
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    def cmd_test(self, code):
        env = {"self": self, "toga": toga, "my_objs": self.my_objs, "Mock": Mock}
        local = {}
        try:
            exec(code, env, local)
            result = local.get("result", env.get("result"))
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


def main():
    return HelloWorld()
