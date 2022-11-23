from unittest.mock import Mock

from pytest import fixture

import toga


@fixture
async def new_widget():
    return toga.Button("")


async def test_press(widget, probe):
    handler = Mock()
    # TODO: can't use set_get, because getattr returns the wrapped handler, which is an
    # implementation detail that we shouldn't expose.
    setattr(widget, "on_press", handler)
    probe.press()
    handler.assert_called_once_with(widget)
