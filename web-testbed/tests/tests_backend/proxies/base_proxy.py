import json
from ..page_singleton import BackgroundPage

class BaseProxy:
    page_provider = staticmethod(lambda: None)

    def _page(self):
        return type(self).page_provider()
    
    def __init__(self, widget_id: str):
        object.__setattr__(self, "_id", widget_id)
   
    @property
    def id(self) -> str:
        return object.__getattribute__(self, "_id")

    @property
    def js_ref(self) -> str:
        return f"self.my_widgets[{repr(self.id)}]"

    @classmethod
    def from_id(cls, widget_id: str) -> "BaseProxy":
        return cls(widget_id)
    
    def _is_function(self, name: str) -> bool:
        prop = repr(name)
        code = (
            f"_obj = {self.js_ref}\n"
            f"_attr = getattr(_obj, {prop})\n"
            f"result = callable(_attr)"
        )
        return bool(self._page().eval_js("(code) => window.test_cmd(code)", code))
    
    def _encode_value(self, value) -> str:
        #other proxy, pass by reference
        if isinstance(value, BaseProxy):
            return value.js_ref
        #if plain primitives, embed as python literal
        if isinstance(value, (str, int, float, bool)) or value is None:
            return repr(value)
        #everything else use text form (what Toga expects for .text, etc)
        return repr(str(value))

    def __setattr__(self, name, value):
        prop = repr(name)

        if name.startswith("_"):
            return object.__setattr__(self, name, value)
        if name == "id":
            raise AttributeError("Proxy 'id' is read-only")        

        rhs = self._encode_value(value)
            
        code = f"setattr({self.js_ref}, {prop}, {rhs})"
        self._page().eval_js("(code) => window.test_cmd(code)", code)

    
    def __getattr__(self, name):
        prop = repr(name)

        # If it's a function on the remote side, return a Python wrapper
        if self._is_function(name):
            def _method(*args):
                parts = [self._encode_value(a) for a in args]
                args_py = ", ".join(parts)
                code = (
                    f"_obj = {self.js_ref}\n"
                    f"_fn = getattr(_obj, {prop})\n"
                    f"result = _fn({args_py})"
                )
                return self._page().eval_js("(code) => window.test_cmd(code)", code)
            return _method

        # else plain property get
        code = f"result = getattr({self.js_ref}, {prop})"
        return self._page().eval_js("(code) => window.test_cmd(code)", code)

    def add_to_main_window(self):
        self._page().eval_js("(code) => window.test_cmd(code)", f"self.main_window.content.add({self.js_ref})")

    def __repr__(self):
        return f"<WidgetProxy id={self.id}>"

    def __str__(self):
        return f"WidgetProxy({self.id})"
    

    