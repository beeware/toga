from .base_proxy import BaseProxy
from .encoding import encode_value


# Since widgets and non-widget objects use this method to be remotely created,
# we now just use 'my_objs' for everything, also makes it simpler than with multiple.
# Also previously had trouble with 'self.widgets'.
class ObjectProxy(BaseProxy):
    def __init__(self, *args, **kwargs):
        key = self._create(self._ctor_expr, *args, **kwargs)
        super().__init__(f"my_objs[{repr(key)}]")

    @classmethod
    def _create(cls, ctor_expr: str, *args, **kwargs) -> str:
        call_args = ", ".join(
            [encode_value(a) for a in args]
            + [f"{k}={encode_value(v)}" for k, v in kwargs.items()]
        )
        code = (
            f"new_obj = {ctor_expr}({call_args})\n"
            "key = str(id(new_obj))\n"
            "self.my_objs[key] = new_obj\n"
            "result = key"
        )
        page = cls._page()
        payload = page.eval_js("(code) => window.test_cmd(code)", code)

        if not (isinstance(payload, dict) and payload.get("type") == "str"):
            raise RuntimeError(f"Unexpected payload creating widget: {payload!r}")

        return payload["value"]
