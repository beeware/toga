import importlib
import sys

import pytest

import toga


def test_factory_module_deprecated():
    """Ensure old factory modules warn when imported."""
    module_name = f"{toga.backend}.factory"
    sys.modules.pop(module_name)
    with pytest.warns(DeprecationWarning):
        importlib.import_module(module_name)
