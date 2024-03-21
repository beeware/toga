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
    return toga.DateInput(on_change=on_change_handler)


@pytest.mark.freeze_time("2023-05-25")
def test_widget_created():
    """A DateInput can be created."""
    widget = toga.DateInput()

    # Round trip the impl/interface
    assert widget._impl.interface == widget
    assert_action_performed(widget, "create DateInput")

    assert widget.value == date(2023, 5, 25)
    assert widget.min == date(1800, 1, 1)
    assert widget.max == date(8999, 12, 31)
    assert widget.on_change._raw is None


def test_widget_created_with_values(on_change_handler):
    """A DateInput can be created with initial values."""
    # Round trip the impl/interface
    widget = toga.DateInput(
        value=date(2015, 6, 15),
        min=date(2013, 5, 14),
        max=date(2017, 7, 16),
        on_change=on_change_handler,
    )
    assert widget._impl.interface == widget
    assert_action_performed(widget, "create DateInput")

    assert widget.value == date(2015, 6, 15)
    assert widget.min == date(2013, 5, 14)
    assert widget.max == date(2017, 7, 16)
    assert widget.on_change._raw == on_change_handler

    # The change handler isn't invoked at construction.
    on_change_handler.assert_not_called()


@pytest.mark.freeze_time("2023-05-25")
@pytest.mark.parametrize(
    "value, expected",
    [
        (date(2023, 1, 11), date(2023, 1, 11)),
        (datetime(2023, 2, 11, 10, 42, 37), date(2023, 2, 11)),
        ("2023-03-11", date(2023, 3, 11)),
        (None, date(2023, 5, 25)),
    ],
)
def test_value(widget, value, expected, on_change_handler):
    """The value of the datepicker can be set."""
    widget.value = value

    assert widget.value == expected

    on_change_handler.assert_called_once_with(widget)


INVALID_VALUES = [
    (123, TypeError, "Not a valid date value"),
    (object(), TypeError, "Not a valid date value"),
    (time(10, 42, 37), TypeError, "Not a valid date value"),
    ("not a date", ValueError, "Invalid isoformat string: 'not a date'"),
]


@pytest.mark.parametrize("value, exc, message", INVALID_VALUES)
def test_invalid_value(widget, value, exc, message):
    """Invalid date values raise an exception."""
    with pytest.raises(exc, match=message):
        widget.value = value


@pytest.mark.parametrize(
    "value, clipped",
    [
        (date(2005, 6, 12), date(2010, 1, 1)),
        (date(2009, 12, 31), date(2010, 1, 1)),
        (date(2010, 1, 1), date(2010, 1, 1)),
        (date(2015, 6, 12), date(2015, 6, 12)),
        (date(2020, 1, 1), date(2020, 1, 1)),
        (date(2020, 1, 2), date(2020, 1, 1)),
        (date(2023, 6, 12), date(2020, 1, 1)),
        # Unlike `min` and `max`, `value` accepts and clips dates outside of the
        # supported range.
        (date(1700, 1, 1), date(2010, 1, 1)),
        (date(9999, 12, 31), date(2020, 1, 1)),
    ],
)
def test_value_clipping(widget, value, clipped, on_change_handler):
    """It the value is inconsistent with min/max, it is clipped."""
    # Set min/max dates, and clear the on_change mock
    widget.min = date(2010, 1, 1)
    widget.max = date(2020, 1, 1)
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
        (None, date(1800, 1, 1)),
        (date(2023, 1, 11), date(2023, 1, 11)),
        (datetime(2023, 2, 11, 10, 42, 37), date(2023, 2, 11)),
        ("2023-03-11", date(2023, 3, 11)),
    ],
)
def test_min(widget, value, expected):
    """The min of the datepicker can be set."""
    widget.min = value

    assert widget.min == expected


INVALID_LIMITS = INVALID_VALUES + [
    (date(1799, 12, 31), ValueError, "The lowest supported date is 1800-01-01"),
    (date(9000, 1, 1), ValueError, "The highest supported date is 8999-12-31"),
]


@pytest.mark.parametrize("value, exc, message", INVALID_LIMITS)
def test_invalid_min(widget, value, exc, message):
    """Invalid min values raise an exception."""
    widget.max = date(2025, 6, 12)

    with pytest.raises(exc, match=message):
        widget.min = value


@pytest.mark.parametrize(
    "min, clip_value, clip_max",
    [
        (date(2005, 6, 1), False, False),
        (date(2005, 6, 25), False, False),
        (date(2005, 6, 26), True, False),
        (date(2005, 7, 4), True, False),
        (date(2005, 12, 31), True, False),
        (date(2006, 1, 1), True, True),
        (date(2006, 7, 4), True, True),
    ],
)
def test_min_clip(widget, on_change_handler, min, clip_value, clip_max):
    """If the current value or max is before a new min date, it is clipped."""
    widget.value = date(2005, 6, 25)
    widget.max = date(2005, 12, 31)
    on_change_handler.reset_mock()

    widget.min = min
    assert widget.min == min

    if clip_value:
        assert widget.value == min
        on_change_handler.assert_called_once_with(widget)
    else:
        assert widget.value == date(2005, 6, 25)
        on_change_handler.assert_not_called()

    if clip_max:
        assert widget.max == min
    else:
        assert widget.max == date(2005, 12, 31)


@pytest.mark.parametrize(
    "value, expected",
    [
        (None, date(8999, 12, 31)),
        (date(2023, 1, 11), date(2023, 1, 11)),
        (datetime(2023, 2, 11, 10, 42, 37), date(2023, 2, 11)),
        ("2023-03-11", date(2023, 3, 11)),
    ],
)
def test_max(widget, value, expected):
    """The max of the datepicker can be set."""
    widget.max = value

    assert widget.max == expected


@pytest.mark.parametrize("value, exc, message", INVALID_LIMITS)
def test_invalid_max(widget, value, exc, message):
    """Invalid max values raise an exception."""
    widget.min = date(2015, 6, 12)

    with pytest.raises(exc, match=message):
        widget.max = value


@pytest.mark.parametrize(
    "max, clip_value, clip_min",
    [
        (date(2005, 6, 1), True, True),
        (date(2005, 6, 24), True, True),
        (date(2005, 6, 25), True, False),
        (date(2005, 7, 4), True, False),
        (date(2005, 12, 30), True, False),
        (date(2005, 12, 31), False, False),
        (date(2006, 7, 4), False, False),
    ],
)
def test_max_clip(widget, on_change_handler, max, clip_value, clip_min):
    """If the current value or min is after a new max date, it is clipped."""
    widget.min = date(2005, 6, 25)
    widget.value = date(2005, 12, 31)
    on_change_handler.reset_mock()

    widget.max = max
    assert widget.max == max

    if clip_value:
        assert widget.value == max
        on_change_handler.assert_called_once_with(widget)
    else:
        assert widget.value == date(2005, 12, 31)
        on_change_handler.assert_not_called()

    if clip_min:
        assert widget.min == max
    else:
        assert widget.min == date(2005, 6, 25)


def test_deprecated_names():
    MIN = date(2012, 8, 3)
    MAX = date(2016, 11, 15)

    with pytest.warns(
        DeprecationWarning, match="DatePicker has been renamed DateInput"
    ), pytest.warns(
        DeprecationWarning, match="DatePicker.min_date has been renamed DateInput.min"
    ), pytest.warns(
        DeprecationWarning, match="DatePicker.max_date has been renamed DateInput.max"
    ):
        widget = toga.DatePicker(min_date=MIN, max_date=MAX)

    assert widget.min == MIN
    assert widget.max == MAX
    widget.min = widget.max = None

    with pytest.warns(
        DeprecationWarning, match="DatePicker.min_date has been renamed DateInput.min"
    ):
        widget.min_date = MIN

    with pytest.warns(
        DeprecationWarning, match="DatePicker.min_date has been renamed DateInput.min"
    ):
        assert widget.min_date == MIN
    assert widget.min == MIN

    with pytest.warns(
        DeprecationWarning, match="DatePicker.max_date has been renamed DateInput.max"
    ):
        widget.max_date = MAX

    with pytest.warns(
        DeprecationWarning, match="DatePicker.max_date has been renamed DateInput.max"
    ):
        assert widget.max_date == MAX
    assert widget.max == MAX

    with pytest.warns(
        DeprecationWarning, match="DatePicker has been renamed DateInput"
    ):
        widget = toga.DatePicker()
    assert widget.min == date(1800, 1, 1)
    assert widget.max == date(8999, 12, 31)
