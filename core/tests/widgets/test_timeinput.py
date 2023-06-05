import datetime
from unittest.mock import Mock

import pytest
from pytest import warns

import toga
from toga_dummy.utils import assert_action_performed


@pytest.fixture
def on_change_handler():
    return Mock()


@pytest.fixture
def widget(on_change_handler):
    return toga.TimeInput(on_change=on_change_handler)


@pytest.mark.freeze_time("2023-05-25 10:42:37")
def test_widget_created():
    """A TimeInput can be created."""
    widget = toga.TimeInput()

    # Round trip the impl/interface
    assert widget._impl.interface == widget
    assert_action_performed(widget, "create TimeInput")

    assert widget.value == datetime.time(10, 42, 0)
    assert widget.on_change._raw is None


def test_widget_created_with_values(on_change_handler):
    """A TimeInput can be created with initial values"""
    # Round trip the impl/interface
    widget = toga.TimeInput(
        value=datetime.time(13, 37, 42),
        min_value=datetime.time(6, 1, 2),
        max_value=datetime.time(18, 58, 59),
        on_change=on_change_handler,
    )
    assert widget._impl.interface == widget
    assert_action_performed(widget, "create TimeInput")

    assert widget.value == datetime.time(13, 37, 42)
    assert widget.min_value == datetime.time(6, 1, 2)
    assert widget.max_value == datetime.time(18, 58, 59)
    assert widget.on_change._raw == on_change_handler

    # The change handler isn't invoked at construction.
    on_change_handler.assert_not_called()


@pytest.mark.freeze_time("2023-05-25 10:42:37")
@pytest.mark.parametrize(
    "value, expected",
    [
        (None, datetime.time(10, 42, 0)),
        (datetime.time(14, 37, 42), datetime.time(14, 37, 42)),
        (datetime.datetime(2023, 2, 11, 14, 37, 42), datetime.time(14, 37, 42)),
        ("14:37:42", datetime.time(14, 37, 42)),
    ],
)
def test_value(widget, value, expected, on_change_handler):
    "The value of the datepicker can be set"
    widget.value = value

    assert widget.value == expected

    on_change_handler.assert_called_once_with(widget)


@pytest.mark.parametrize(
    "value, exc, message",
    [
        (123, TypeError, "Not a valid time value"),
        (object(), TypeError, "Not a valid time value"),
        (datetime.date(2023, 5, 25), TypeError, "Not a valid time value"),
        ("not a time", ValueError, "Invalid isoformat string: 'not a time'"),
    ],
)
def test_invalid_value(widget, value, exc, message):
    "Invalid time values raise an exception"
    with pytest.raises(exc, match=message):
        widget.value = value


@pytest.mark.parametrize(
    "value, clipped",
    [
        (datetime.time(3, 37, 42), datetime.time(6, 0, 0)),
        (datetime.time(10, 37, 42), datetime.time(10, 37, 42)),
        (datetime.time(22, 37, 42), datetime.time(18, 0, 0)),
    ],
)
def test_value_clipping(widget, value, clipped, on_change_handler):
    "It the value is inconsistent with min/max, it is clipped."
    # Set min/max dates, and clear the on_change mock
    widget.min_value = datetime.time(6, 0, 0)
    widget.max_value = datetime.time(18, 0, 0)
    on_change_handler.reset_mock()

    # Set the new value
    widget.value = value

    # Value has been clipped
    assert widget.value == clipped

    # on_change handler called once.
    on_change_handler.assert_called_once_with(widget)


@pytest.mark.parametrize(
    "value, expected",
    [
        (None, None),
        (datetime.time(6, 1, 11), datetime.time(6, 1, 11)),
        (datetime.datetime(2023, 6, 16, 6, 2, 11), datetime.time(6, 2, 11)),
        ("06:03:11", datetime.time(6, 3, 11)),
    ],
)
def test_min_value(widget, value, expected):
    "The min_value of the datepicker can be set"
    widget.min_value = value

    assert widget.min_value == expected


@pytest.mark.parametrize(
    "value, exc, message",
    [
        (123, TypeError, "Not a valid time value"),
        (object(), TypeError, "Not a valid time value"),
        (datetime.date(2023, 5, 25), TypeError, "Not a valid time value"),
        ("not a time", ValueError, "Invalid isoformat string: 'not a time'"),
        (
            datetime.time(19, 0, 0),
            ValueError,
            "min_value is after the current max_value",
        ),
    ],
)
def test_invalid_min_value(widget, value, exc, message):
    "Invalid min_value values raise an exception"
    widget.max_value = datetime.time(18, 0, 0)

    with pytest.raises(exc, match=message):
        widget.min_value = value


def test_min_value_clip(widget, on_change_handler):
    "If the current value is before a new min date, the value is clipped"
    widget.value = datetime.time(3, 42, 37)

    # Clear the change handler
    on_change_handler.reset_mock()

    widget.min_value = datetime.time(6, 0, 0)

    # Value has been clipped
    assert widget.value == datetime.time(6, 0, 0)

    # on_change handler called.
    on_change_handler.assert_called_once_with(widget)


@pytest.mark.parametrize(
    "value, expected",
    [
        (None, None),
        (datetime.time(18, 1, 11), datetime.time(18, 1, 11)),
        (datetime.datetime(2023, 5, 25, 18, 2, 11), datetime.time(18, 2, 11)),
        ("18:03:11", datetime.time(18, 3, 11)),
    ],
)
def test_max_value(widget, value, expected):
    "The max_value of the datepicker can be set"
    widget.max_value = value

    assert widget.max_value == expected


@pytest.mark.parametrize(
    "value, exc, message",
    [
        (123, TypeError, "Not a valid time value"),
        (object(), TypeError, "Not a valid time value"),
        (datetime.date(2023, 5, 25), TypeError, "Not a valid time value"),
        ("not a time", ValueError, "Invalid isoformat string: 'not a time'"),
        (
            datetime.time(6, 37, 42),
            ValueError,
            "max_value is before the current min_value",
        ),
    ],
)
def test_invalid_max_value(widget, value, exc, message):
    "Invalid max_value values raise an exception"
    widget.min_value = datetime.time(18, 0, 0)

    with pytest.raises(exc, match=message):
        widget.max_value = value


def test_max_value_clip(widget, on_change_handler):
    "If the current value is after a new max date, the value is clipped"
    widget.value = datetime.time(22, 37, 42)

    # Clear the change handler
    on_change_handler.reset_mock()

    widget.max_value = datetime.time(18, 0, 0)

    # Value has been clipped
    assert widget.value == datetime.time(18, 0, 0)

    # on_change handler called.
    on_change_handler.assert_called_once_with(widget)


def test_deprecated_names():
    MIN = datetime.time(8, 30, 59)
    MAX = datetime.time(10, 0, 0)

    with warns(DeprecationWarning, match="TimePicker has been renamed TimeInput"):
        widget = toga.TimePicker(min_time=MIN, max_time=MAX)
    assert widget.min_value == MIN
    assert widget.max_value == MAX
    widget.min_value = widget.max_value = None

    widget.min_time = MIN
    assert widget.min_time == MIN
    assert widget.min_value == MIN

    widget.max_time = MAX
    assert widget.max_time == MAX
    assert widget.max_value == MAX
