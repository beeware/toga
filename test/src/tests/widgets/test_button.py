from unittest.mock import Mock

from pytest import fixture
from System import EventArgs

import toga

from ..test_utils import set_get


@fixture
async def widget(main_box):
    button = toga.Button("")
    main_box.add(button)
    yield button
    main_box.remove(button)


async def test_on_press(widget, native):
    handler = Mock()
    # FIXME: getattr returns the wrapped handler, which is an implementation detail that
    # we shouldn't expose.
    set_get(widget, "on_press", handler)
    native.OnClick(EventArgs.Empty)
    handler.assert_called_once_with(widget)
