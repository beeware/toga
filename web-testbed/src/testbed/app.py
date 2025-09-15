import uuid

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
    to_js = None


class HelloWorld(toga.App):
    def startup(self):
        main_box = toga.Box(style=Pack(direction=COLUMN))
        self.label = toga.Label(id="myLabel", text="Test App - Toga Web Testing")

        if js is not None:
            js.window.test_cmd = create_proxy(self.cmd_test)

        main_box.add(self.label)
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    def _is_primitive(self, v):
        return isinstance(v, (type(None), bool, int, float, str))

    def _serialize(self, v):
        if self._is_primitive(v):
            return v
        if isinstance(v, list):
            return [self._serialize(x) for x in v]
        if isinstance(v, dict):
            return {k: self._serialize(x) for k, x in v.items()}

        wid = getattr(v, "id", None)
        if wid is not None:
            self.my_widgets[wid] = v
            return {
                "$t": "handle",
                "ns": "widgets",
                "class": type(v).__name__,
                "id": wid,
            }

        hid = f"h_{uuid.uuid4().hex[:10]}"
        self.my_objs[hid] = v
        return {"$t": "handle", "ns": "handles", "class": type(v).__name__, "id": hid}

    def cmd_test(self, code):
        local_vars = {}
        try:
            exec(code, {"self": self, "toga": toga}, local_vars)
            result = local_vars.get("result", None)
            result = self._serialize(result)

            if js is not None and to_js is not None:
                # dicts become plain JS Objects
                result = to_js(result, dict_converter=js.Object.fromEntries)

            return result
        except Exception as e:
            return f"Error: {e}"


def main():
    return HelloWorld()
