import importlib
import sys
import types

import pytest

from .playwright_page import BackgroundPage
from .proxies.base_proxy import BaseProxy
from .proxies.object_proxies import (
    AppProxy,
    BoxProxy,
    ButtonProxy,
    DateInputProxy,
    LabelProxy,
    MockProxy,
    PasswordInputProxy,
    SwitchProxy,
    TextInputProxy,
    TimeInputProxy,
)
from .widgets.base import SimpleProbe

# Playwright Page injection


@pytest.fixture(scope="session")
def page():
    p = BackgroundPage()
    return p


@pytest.fixture(scope="session", autouse=True)
def _wire_page(page):
    BaseProxy.page_provider = staticmethod(lambda: page)
    SimpleProbe.page_provider = staticmethod(lambda: page)


# Shims

SHIMS = [
    ("toga", "App.app", AppProxy),
    ("toga", "Button", ButtonProxy),
    ("toga", "Box", BoxProxy),
    ("toga", "Label", LabelProxy),
    ("toga", "Switch", SwitchProxy),
    ("toga", "TextInput", TextInputProxy),
    ("toga", "PasswordInput", PasswordInputProxy),
    ("toga", "TimeInput", TimeInputProxy),
    ("toga", "DateInput", DateInputProxy),
    ("unittest.mock", "Mock", MockProxy),
]


def apply():
    for mod_name, dotted_attr, spec in SHIMS:
        try:
            mod = importlib.import_module(mod_name)
        except Exception:
            if mod_name.startswith("toga"):
                mod = types.ModuleType(mod_name)
                sys.modules[mod_name] = mod
            else:
                raise

        parts = dotted_attr.split(".")
        target = mod
        for part in parts[:-1]:
            if not hasattr(target, part):
                setattr(target, part, types.SimpleNamespace())
            target = getattr(target, part)

        setattr(target, parts[-1], spec)


apply()
