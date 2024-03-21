from datetime import date, datetime, time
from unittest.mock import Mock

import pytest

import toga
from toga_dummy.utils import assert_action_performed


@pytest.fixture
def on_change_handler():
    return Mock()


@pytest.fixture
def widget(on_change_handler):
    return toga.TimeInput(on_change=on_change_handler)


@pytest.mark.freeze_time("2023-05-25 10:42:37.123456")
def test_widget_created():
    """A TimeInput can be created."""
    widget = toga.TimeInput()

    # Round trip the impl/interface
    assert widget._impl.interface == widget
    assert_action_performed(widget, "create TimeInput")

    assert widget.value == time(10, 42, 37)
    assert widget.on_change._raw is None


def test_widget_created_with_values(on_change_handler):
    """A TimeInput can be created with initial values."""
    # Round trip the impl/interface
    widget = toga.TimeInput(
        value=time(13, 37, 42),
        min=time(6, 1, 2),
        max=time(18, 58, 59),
        on_change=on_change_handler,
    )
    assert widget._impl.interface == widget
    assert_action_performed(widget, "create TimeInput")

    assert widget.value == time(13, 37, 42)
    assert widget.min == time(6, 1, 2)
    assert widget.max == time(18, 58, 59)
    assert widget.on_change._raw == on_change_handler

    # The change handler isn't invoked at construction.
    on_change_handler.assert_not_called()


@pytest.mark.freeze_time("2023-05-25 10:42:37.123456")
@pytest.mark.parametrize(
    "value, expected",
    [
        (time(14, 37, 42, 123456), time(14, 37, 42)),
        (datetime(2023, 2, 11, 14, 37, 42, 123456), time(14, 37, 42)),
        ("14:37:42.123456", time(14, 37, 42)),
        (None, time(10, 42, 37)),
    ],
)
def test_value(widget, value, expected, on_change_handler):
    """The value of the datepicker can be set."""
    widget.value = value

    assert widget.value == expected

    on_change_handler.assert_called_once_with(widget)


INVALID_VALUES = [
    (123, TypeError, "Not a valid time value"),
    (object(), TypeError, "Not a valid time value"),
    (date(2023, 5, 25), TypeError, "Not a valid time value"),
    ("not a time", ValueError, "Invalid isoformat string: 'not a time'"),
]


@pytest.mark.parametrize("value, exc, message", INVALID_VALUES)
def test_invalid_value(widget, value, exc, message):
    """Invalid time values raise an exception."""
    with pytest.raises(exc, match=message):
        widget.value = value


@pytest.mark.parametrize(
    "value, clipped",
    [
        (time(3, 37, 42), time(6, 0, 0)),
        (time(5, 59, 59), time(6, 0, 0)),
        (time(6, 0, 0), time(6, 0, 0)),
        (time(10, 37, 42), time(10, 37, 42)),
        (time(18, 0, 0), time(18, 0, 0)),
        (time(18, 0, 1), time(18, 0, 0)),
        (time(22, 37, 42), time(18, 0, 0)),
    ],
)
def test_value_clipping(widget, value, clipped, on_change_handler):
    """It the value is inconsistent with min/max, it is clipped."""
    # Set min/max dates, and clear the on_change mock
    widget.min = time(6, 0, 0)
    widget.max = time(18, 0, 0)
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
        (None, time(0, 0, 0)),
        (time(6, 1, 11), time(6, 1, 11)),
        (datetime(2023, 6, 16, 6, 2, 11), time(6, 2, 11)),
        ("06:03:11", time(6, 3, 11)),
    ],
)
def test_min(widget, value, expected):
    """The min of the datepicker can be set."""
    widget.min = value

    assert widget.min == expected


@pytest.mark.parametrize("value, exc, message", INVALID_VALUES)
def test_invalid_min(widget, value, exc, message):
    """Invalid min values raise an exception."""
    widget.max = time(18, 0, 0)

    with pytest.raises(exc, match=message):
        widget.min = value


@pytest.mark.parametrize(
    "min, clip_value, clip_max",
    [
        (time(1, 2, 3), False, False),
        (time(3, 42, 37), False, False),
        (time(3, 42, 38), True, False),
        (time(6, 0, 0), True, False),
        (time(12, 0, 0), True, False),
        (time(12, 0, 1), True, True),
        (time(13, 14, 15), True, True),
    ],
)
def test_min_clip(widget, on_change_handler, min, clip_value, clip_max):
    """If the current value or max is before a new min time, it is clipped."""
    widget.value = time(3, 42, 37)
    widget.max = time(12, 0, 0)
    on_change_handler.reset_mock()

    widget.min = min
    assert widget.min == min

    if clip_value:
        assert widget.value == min
        on_change_handler.assert_called_once_with(widget)
    else:
        assert widget.value == time(3, 42, 37)
        on_change_handler.assert_not_called()

    if clip_max:
        assert widget.max == min
    else:
        assert widget.max == time(12, 0, 0)


@pytest.mark.parametrize(
    "value, expected",
    [
        (None, time(23, 59, 59)),
        (time(18, 1, 11), time(18, 1, 11)),
        (datetime(2023, 5, 25, 18, 2, 11), time(18, 2, 11)),
        ("18:03:11", time(18, 3, 11)),
    ],
)
def test_max(widget, value, expected):
    """The max of the datepicker can be set."""
    widget.max = value

    assert widget.max == expected


@pytest.mark.parametrize("value, exc, message", INVALID_VALUES)
def test_invalid_max(widget, value, exc, message):
    """Invalid max values raise an exception."""
    widget.min = time(18, 0, 0)

    with pytest.raises(exc, match=message):
        widget.max = value


@pytest.mark.parametrize(
    "max, clip_value, clip_min",
    [
        (time(1, 2, 3), True, True),
        (time(3, 42, 36), True, True),
        (time(3, 42, 37), True, False),
        (time(6, 0, 0), True, False),
        (time(11, 59, 0), True, False),
        (time(12, 0, 0), False, False),
        (time(13, 14, 15), False, False),
    ],
)
def test_max_clip(widget, on_change_handler, max, clip_value, clip_min):
    """If the current value is after a new max date, the value is clipped."""
    widget.min = time(3, 42, 37)
    widget.value = time(12, 0, 0)
    on_change_handler.reset_mock()

    widget.max = max
    assert widget.max == max

    if clip_value:
        assert widget.value == max
        on_change_handler.assert_called_once_with(widget)
    else:
        assert widget.value == time(12, 0, 0)
        on_change_handler.assert_not_called()

    if clip_min:
        assert widget.min == max
    else:
        assert widget.min == time(3, 42, 37)


def test_deprecated_names():
    MIN = time(8, 30, 59)
    MAX = time(10, 0, 0)

    with pytest.warns(
        DeprecationWarning, match="TimePicker has been renamed TimeInput"
    ), pytest.warns(
        DeprecationWarning, match="TimePicker.min_time has been renamed TimeInput.min"
    ), pytest.warns(
        DeprecationWarning, match="TimePicker.max_time has been renamed TimeInput.max"
    ):
        widget = toga.TimePicker(min_time=MIN, max_time=MAX)

    assert widget.min == MIN
    assert widget.max == MAX
    widget.min = widget.max = None

    with pytest.warns(
        DeprecationWarning, match="TimePicker.min_time has been renamed TimeInput.min"
    ):
        widget.min_time = MIN

    with pytest.warns(
        DeprecationWarning, match="TimePicker.min_time has been renamed TimeInput.min"
    ):
        assert widget.min_time == MIN
    assert widget.min == MIN

    with pytest.warns(
        DeprecationWarning, match="TimePicker.max_time has been renamed TimeInput.max"
    ):
        widget.max_time = MAX

    with pytest.warns(
        DeprecationWarning, match="TimePicker.max_time has been renamed TimeInput.max"
    ):
        assert widget.max_time == MAX
    assert widget.max == MAX

    with pytest.warns(
        DeprecationWarning, match="TimePicker has been renamed TimeInput"
    ):
        widget = toga.TimePicker()
    assert widget.min == time(0, 0, 0)
    assert widget.max == time(23, 59, 59)
