from importlib import import_module

def get_probe(widget):
    name = type(widget).__name__          # e.g. "ButtonProxy"
    base = name.removesuffix("Proxy")     # -> "Button"
    module = import_module(f"tests.tests_backend.widgets.{base.lower()}")  # -> tests/tests_backend/widgets/button.py
    return getattr(module, f"{base}Probe")(widget)
