import sys
from dataclasses import dataclass
from unittest.mock import Mock

import pytest

if sys.version_info < (3, 10):
    _DATACLASS_KWARGS = {"init": False}
else:
    _DATACLASS_KWARGS = {"kw_only": True}

from travertino.colors import hsl, hsla, rgb, rgba


def prep_style_class(cls):
    """Decorator to apply dataclass and mock apply."""
    return mock_attr("apply")(dataclass(**_DATACLASS_KWARGS)(cls))


def mock_attr(attr):
    """Mock an arbitrary attribute of a class."""

    def returned_decorator(cls):
        orig_init = cls.__init__

        def __init__(self, *args, **kwargs):
            setattr(self, attr, Mock())
            orig_init(self, *args, **kwargs)

        cls.__init__ = __init__
        return cls

    return returned_decorator


def assert_equal_color(actual, expected, tolerance=None, blend=False, unblend=False):
    if {True} in {blend, unblend}:
        tolerance = 1e-6

    if {type(actual), type(expected)} == {rgba}:
        assert actual.rgba.r == pytest.approx(expected.rgba.r, abs=tolerance)
        assert actual.rgba.g == pytest.approx(expected.rgba.g, abs=tolerance)
        assert actual.rgba.b == pytest.approx(expected.rgba.b, abs=tolerance)
        assert actual.rgba.a == pytest.approx(expected.rgba.a, abs=tolerance)
    elif {type(actual), type(expected)} == {rgb}:
        assert actual.rgb.r == pytest.approx(expected.rgb.r, abs=tolerance)
        assert actual.rgb.g == pytest.approx(expected.rgb.g, abs=tolerance)
        assert actual.rgb.b == pytest.approx(expected.rgb.b, abs=tolerance)
    elif {type(actual), type(expected)} == {hsla}:
        assert actual.hsla.h == pytest.approx(expected.hsla.h, abs=tolerance)
        assert actual.hsla.s == pytest.approx(expected.hsla.s, abs=tolerance)
        assert actual.hsla.l == pytest.approx(expected.hsla.l, abs=tolerance)
        assert actual.hsla.a == pytest.approx(expected.hsla.a, abs=tolerance)
    elif {type(actual), type(expected)} == {hsl}:
        assert actual.hsl.h == pytest.approx(expected.hsl.h, abs=tolerance)
        assert actual.hsl.s == pytest.approx(expected.hsl.s, abs=tolerance)
        assert actual.hsl.l == pytest.approx(expected.hsl.l, abs=tolerance)
    else:
        raise ValueError(
            "Actual color and expected color should be of the same type. "
            f"But got actual:{type(actual)} and expected:{type(expected)}."
        )
