from unittest.mock import Mock

from pytest import fixture
from System import EventArgs
from tests.utils import set_get

import toga


@fixture
def widget(main_box):
    button = toga.Button("")
    main_box.add(button)
    yield button
    main_box.remove(button)


def test_on_press(widget, native):
    handler = Mock()
    set_get(widget, "on_press", handler)
    native.OnClick(EventArgs.Empty)
    handler.assert_called_once_with(widget)
