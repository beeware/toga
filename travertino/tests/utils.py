import sys
from copy import deepcopy
from dataclasses import dataclass
from unittest.mock import Mock

import pytest

from travertino.colors import hsl, rgb

if sys.version_info < (3, 10):
    _DATACLASS_KWARGS = {"init": False, "repr": False}
else:
    _DATACLASS_KWARGS = {"kw_only": True, "repr": False}


def apply_dataclass(cls):
    """Decorator to apply dataclass with arguments depending on Python version"""
    return dataclass(**_DATACLASS_KWARGS)(cls)


def mock_apply(cls):
    """Mock a style class's apply() method."""
    orig_init = cls.__init__

    def __init__(self, *args, **kwargs):
        self.apply = Mock(wraps=self.apply)
        # The argument to _apply is a (mutable) set that will be cleared, so a copy
        # needs to be saved to check against.
        self._apply = CopyingMock()
        orig_init(self, *args, **kwargs)

    cls.__init__ = __init__
    return cls


class CopyingMock(Mock):
    """Mock that copies rather than references its call args, for mutable arguments.

    Stripped-down version of example from:
    https://docs.python.org/3.13//library/unittest.mock-examples.html
    #coping-with-mutable-arguments
    """

    def __call__(self, *args):
        return super().__call__(*deepcopy(args))


def assert_equal_color(actual, expected, abs=1e-6):
    if type(actual) is type(expected) is rgb:
        assert actual.r == pytest.approx(expected.r, abs=abs)
        assert actual.g == pytest.approx(expected.g, abs=abs)
        assert actual.b == pytest.approx(expected.b, abs=abs)
        assert actual.a == pytest.approx(expected.a, abs=abs)
    elif type(actual) is type(expected) is hsl:
        if not (actual.s == 0 or actual.l in {0, 1}):
            # Don't test hue if color is white/black/grey.
            assert actual.h == pytest.approx(expected.h, abs=abs)
        assert actual.s == pytest.approx(expected.s, abs=abs)
        assert actual.l == pytest.approx(expected.l, abs=abs)
        assert actual.a == pytest.approx(expected.a, abs=abs)
    else:
        raise ValueError(
            "Actual color and expected color should be of the same type. "
            f"But got actual: {type(actual)} and expected: {type(expected)}."
        )
