from unittest.mock import Mock

from pytest import fixture

import toga
from toga.colors import TRANSPARENT

from ..assertions import assert_color
from .properties import (  # noqa: F401
    test_background_color,
    test_color,
    test_text,
)


@fixture
async def widget():
    return toga.Button("")


async def test_press(widget, probe):
    handler = Mock()
    # TODO: can't use assert_set_get, because getattr returns the wrapped handler, which
    # is an implementation detail that we shouldn't expose.
    # https://github.com/beeware/toga/pull/804 may be relevant.
    setattr(widget, "on_press", handler)
    probe.press()
    handler.assert_called_once_with(widget)


async def test_background_color_transparent(widget, probe):
    "Buttons treat background transparency as a color reset."
    widget.style.background_color = TRANSPARENT
    assert_color(probe.background_color, None)
