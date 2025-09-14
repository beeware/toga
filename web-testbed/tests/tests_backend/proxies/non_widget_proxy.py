from .base_proxy import BaseProxy


class NonWidgetProxy(BaseProxy):
    # Using my_widgets for all objects for now
    # _storage_expr = "self.my_objs"
    # _ctor_expr: str | None = None

    def _create(self, ctor_expr: str, *args, **kwargs) -> str:
        call_args = self._encode_call(*args, **kwargs)
        code = (
            "import uuid\n"
            f"new_obj = {ctor_expr}({call_args})\n"
            "key = str(uuid.uuid4())\n"
            "self.my_widgets[key] = new_obj\n"
            "result = key"
        )
        return self._page().eval_js("(code) => window.test_cmd(code)", code)
