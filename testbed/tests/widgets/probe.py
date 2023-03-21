from importlib import import_module

import pytest


def get_probe(widget):
    name = type(widget).__name__

    try:
        module = import_module(f"tests_backend.widgets.{name.lower()}")
        return getattr(module, f"{name}Probe")(widget)
    except ModuleNotFoundError:
        pytest.skip(f"No platform probe module found for widget {name!r}")
    except AttributeError:
        pytest.skip(f"No platform probe found for widget {name!r}")
