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
    return toga.DateInput(on_change=on_change_handler)


@pytest.mark.freeze_time("2023-05-25")
def test_widget_created():
    """A DateInput can be created."""
    widget = toga.DateInput()

    # Round trip the impl/interface
    assert widget._impl.interface == widget
    assert_action_performed(widget, "create DateInput")

    assert widget.value == datetime.date(2023, 5, 25)
    assert widget.on_change._raw is None


def test_widget_created_with_values(on_change_handler):
    """A DateInput can be created with initial values"""
    # Round trip the impl/interface
    widget = toga.DateInput(
        value=datetime.date(2015, 6, 15),
        min_value=datetime.date(2013, 5, 14),
        max_value=datetime.date(2017, 7, 16),
        on_change=on_change_handler,
    )
    assert widget._impl.interface == widget
    assert_action_performed(widget, "create DateInput")

    assert widget.value == datetime.date(2015, 6, 15)
    assert widget.min_value == datetime.date(2013, 5, 14)
    assert widget.max_value == datetime.date(2017, 7, 16)
    assert widget.on_change._raw == on_change_handler

    # The change handler isn't invoked at construction.
    on_change_handler.assert_not_called()


@pytest.mark.freeze_time("2023-05-25")
@pytest.mark.parametrize(
    "value, expected",
    [
        (None, datetime.date(2023, 5, 25)),
        (datetime.date(2023, 1, 11), datetime.date(2023, 1, 11)),
        (datetime.datetime(2023, 2, 11, 10, 42, 37), datetime.date(2023, 2, 11)),
        ("2023-03-11", datetime.date(2023, 3, 11)),
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
        (123, TypeError, "Not a valid date value"),
        (object(), TypeError, "Not a valid date value"),
        (datetime.time(10, 42, 37), TypeError, "Not a valid date value"),
        ("not a date", ValueError, "Invalid isoformat string: 'not a date'"),
    ],
)
def test_invalid_value(widget, value, exc, message):
    "Invalid date values raise an exception"
    with pytest.raises(exc, match=message):
        widget.value = value


@pytest.mark.parametrize(
    "value, clipped",
    [
        (datetime.date(2005, 6, 12), datetime.date(2010, 1, 1)),
        (datetime.date(2015, 6, 12), datetime.date(2015, 6, 12)),
        (datetime.date(2023, 6, 12), datetime.date(2020, 1, 1)),
    ],
)
def test_value_clipping(widget, value, clipped, on_change_handler):
    "It the value is inconsistent with min/max, it is clipped."
    # Set min/max dates, and clear the on_change mock
    widget.min_value = datetime.date(2010, 1, 1)
    widget.max_value = datetime.date(2020, 1, 1)
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
        (datetime.date(2023, 1, 11), datetime.date(2023, 1, 11)),
        (datetime.datetime(2023, 2, 11, 10, 42, 37), datetime.date(2023, 2, 11)),
        ("2023-03-11", datetime.date(2023, 3, 11)),
    ],
)
def test_min_value(widget, value, expected):
    "The min_value of the datepicker can be set"
    widget.min_value = value

    assert widget.min_value == expected


@pytest.mark.parametrize(
    "value, exc, message",
    [
        (123, TypeError, "Not a valid date value"),
        (object(), TypeError, "Not a valid date value"),
        (datetime.time(10, 42, 37), TypeError, "Not a valid date value"),
        ("not a date", ValueError, "Invalid isoformat string: 'not a date'"),
        (
            datetime.date(2049, 1, 1),
            ValueError,
            "min_value is after the current max_value",
        ),
    ],
)
def test_invalid_min_value(widget, value, exc, message):
    "Invalid min_value values raise an exception"
    widget.max_value = datetime.date(2025, 6, 12)

    with pytest.raises(exc, match=message):
        widget.min_value = value


def test_min_value_clip(widget, on_change_handler):
    "If the current value is before a new min date, the value is clipped"
    widget.value = datetime.date(2005, 6, 25)

    # Clear the change handler
    on_change_handler.reset_mock()

    widget.min_value = datetime.date(2010, 1, 1)

    # Value has been clipped
    assert widget.value == datetime.date(2010, 1, 1)

    # on_change handler called.
    on_change_handler.assert_called_once_with(widget)


@pytest.mark.parametrize(
    "value, expected",
    [
        (None, None),
        (datetime.date(2023, 1, 11), datetime.date(2023, 1, 11)),
        (datetime.datetime(2023, 2, 11, 10, 42, 37), datetime.date(2023, 2, 11)),
        ("2023-03-11", datetime.date(2023, 3, 11)),
    ],
)
def test_max_value(widget, value, expected):
    "The max_value of the datepicker can be set"
    widget.max_value = value

    assert widget.max_value == expected


@pytest.mark.parametrize(
    "value, exc, message",
    [
        (123, TypeError, "Not a valid date value"),
        (object(), TypeError, "Not a valid date value"),
        (datetime.time(10, 42, 37), TypeError, "Not a valid date value"),
        ("not a date", ValueError, "Invalid isoformat string: 'not a date'"),
        (
            datetime.date(2001, 1, 1),
            ValueError,
            "max_value is before the current min_value",
        ),
    ],
)
def test_invalid_max_value(widget, value, exc, message):
    "Invalid max_value values raise an exception"
    widget.min_value = datetime.date(2015, 6, 12)

    with pytest.raises(exc, match=message):
        widget.max_value = value


def test_max_value_clip(widget, on_change_handler):
    "If the current value is after a new max date, the value is clipped"
    widget.value = datetime.date(2012, 6, 25)

    # Clear the change handler
    on_change_handler.reset_mock()

    widget.max_value = datetime.date(2010, 1, 1)

    # Value has been clipped
    assert widget.value == datetime.date(2010, 1, 1)

    # on_change handler called.
    on_change_handler.assert_called_once_with(widget)


def test_deprecated_names():
    MIN = datetime.date(2012, 8, 3)
    MAX = datetime.date(2016, 11, 15)

    with warns(DeprecationWarning, match="DatePicker has been renamed DateInput"):
        widget = toga.DatePicker(min_date=MIN, max_date=MAX)
    assert widget.min_value == MIN
    assert widget.max_value == MAX
    widget.min_value = widget.max_value = None

    widget.min_date = MIN
    assert widget.min_date == MIN
    assert widget.min_value == MIN

    widget.max_date = MAX
    assert widget.max_date == MAX
    assert widget.max_value == MAX
