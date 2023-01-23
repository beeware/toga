from importlib import import_module

from pytest import skip


def get_probe(widget):
    name = type(widget).__name__
    try:
        module = import_module(f"tests_backend.widgets.{name.lower()}")
    except ModuleNotFoundError as e:
        skip(f"No probe module for {name} ({e})")
    return getattr(module, f"{name}Probe")(widget)
