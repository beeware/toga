import importlib
import sys

import pytest

import toga

from .conftest import skip_on_backends

skip_on_backends(
    "toga_winui3",
    reason="Factory modules are not implemented on this backend.",
    allow_module_level=True,
)


async def test_factory_module_deprecated():
    """Ensure old factory modules warn when imported."""
    module_name = f"{toga.backend}.factory"
    sys.modules.pop(module_name, None)
    with pytest.warns(DeprecationWarning):
        importlib.import_module(module_name)
