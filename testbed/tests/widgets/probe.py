from importlib import import_module


def get_probe(widget):
    name = type(widget).__name__
    module = import_module(f"tests_backend.widgets.{name.lower()}")
    return getattr(module, f"{name}Probe")(widget)
