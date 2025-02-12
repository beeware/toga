import sys
from dataclasses import dataclass
from unittest.mock import Mock

import pytest

from travertino.colors import hsl, hsla, rgb, rgba

if sys.version_info < (3, 10):
    _DATACLASS_KWARGS = {"init": False}
else:
    _DATACLASS_KWARGS = {"kw_only": True}


def apply_dataclass(cls):
    """Decorator to apply dataclass with arguments depending on Python version"""
    return dataclass(**_DATACLASS_KWARGS)(cls)


def mock_apply(cls):
    """Mock a style class's apply() method.

    Because apply() is called with or without arguments in different circumstances, and
    due to limited granularity in Mock's assertions (e.g. you can't check that multiple
    calls are there, but no other calls), the two usages are dispatched to separate
    mocks.
    """
    orig_init = cls.__init__

    def apply(self, *args, **kwargs):
        if args or kwargs:
            self._apply_names(*args, **kwargs)
        else:
            self._apply_all()

    def reset_mocks(self):
        self._apply_names.reset_mock()
        self._apply_all.reset_mock()

    cls.apply = apply
    cls._reset_mocks = reset_mocks

    def __init__(self, *args, **kwargs):
        self._apply_names = Mock()
        self._apply_all = Mock()
        orig_init(self, *args, **kwargs)

    cls.__init__ = __init__
    return cls


def assert_equal_color(actual, expected, abs=1e-6):
    if {type(actual), type(expected)} == {rgba}:
        assert actual.rgba.r == pytest.approx(expected.rgba.r, abs=abs)
        assert actual.rgba.g == pytest.approx(expected.rgba.g, abs=abs)
        assert actual.rgba.b == pytest.approx(expected.rgba.b, abs=abs)
        assert actual.rgba.a == pytest.approx(expected.rgba.a, abs=abs)
    elif {type(actual), type(expected)} == {rgb}:
        assert actual.rgb.r == pytest.approx(expected.rgb.r, abs=abs)
        assert actual.rgb.g == pytest.approx(expected.rgb.g, abs=abs)
        assert actual.rgb.b == pytest.approx(expected.rgb.b, abs=abs)
    elif {type(actual), type(expected)} == {hsla}:
        assert actual.hsla.h == pytest.approx(expected.hsla.h, abs=abs)
        assert actual.hsla.s == pytest.approx(expected.hsla.s, abs=abs)
        assert actual.hsla.l == pytest.approx(expected.hsla.l, abs=abs)
        assert actual.hsla.a == pytest.approx(expected.hsla.a, abs=abs)
    elif {type(actual), type(expected)} == {hsl}:
        assert actual.hsl.h == pytest.approx(expected.hsl.h, abs=abs)
        assert actual.hsl.s == pytest.approx(expected.hsl.s, abs=abs)
        assert actual.hsl.l == pytest.approx(expected.hsl.l, abs=abs)
    else:
        raise ValueError(
            "Actual color and expected color should be of the same type. "
            f"But got actual:{type(actual)} and expected:{type(expected)}."
        )
