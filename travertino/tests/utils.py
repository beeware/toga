import sys
from dataclasses import dataclass
from unittest.mock import Mock

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


def assert_equal_color(
    actual, expected, tolerance=1e-2, alpha_unblending_operation=False
):
    try:
        if {type(actual), type(expected)} == {rgba}:
            assert abs(actual.rgba.r - expected.rgba.r) < tolerance
            assert abs(actual.rgba.g - expected.rgba.g) < tolerance
            assert abs(actual.rgba.b - expected.rgba.b) < tolerance
            assert abs(actual.rgba.a - expected.rgba.a) < tolerance
        elif {type(actual), type(expected)} == {rgb}:
            assert abs(actual.rgb.r - expected.rgb.r) < tolerance
            assert abs(actual.rgb.g - expected.rgb.g) < tolerance
            assert abs(actual.rgb.b - expected.rgb.b) < tolerance
        elif {type(actual), type(expected)} == {hsla}:
            # Unblending hsla color, sometimes produces slightly
            # imprecise original front_color, as the alpha blending
            # calculation is done on rgba values, and some amount
            # of precision is lost during the conversions. Hence,
            # assert deblended color with slightly higher tolerance.
            assert (
                abs(actual.hsla.h - expected.hsla.h) < 1.4
                if alpha_unblending_operation
                else tolerance
            )
            assert (
                abs(actual.hsla.s - expected.hsla.s) < 0.05
                if alpha_unblending_operation
                else tolerance
            )
            assert abs(actual.hsla.l - expected.hsla.l) < tolerance
            assert abs(actual.hsla.a - expected.hsla.a) < tolerance
        elif {type(actual), type(expected)} == {hsl}:
            assert abs(actual.hsl.h - expected.hsl.h) < tolerance
            assert abs(actual.hsl.s - expected.hsl.s) < tolerance
            assert abs(actual.hsl.l - expected.hsl.l) < tolerance
        else:
            raise ValueError(
                "Actual color and expected color should be of the same type. "
                f"But got actual:{type(actual)} and expected:{type(expected)}."
            )
    except AssertionError as error:
        error.add_note(f"actual: {actual}, expected: {expected}")
        raise error
