from decimal import Decimal
from unittest.mock import Mock

import pytest

import toga
from toga.widgets.numberinput import _clean_decimal_str
from toga_dummy.utils import (
    EventLog,
    assert_action_performed,
    attribute_value,
)


@pytest.fixture
def widget():
    return toga.NumberInput()


def test_widget_created(widget):
    "A text input can be created"
    assert widget._impl.interface == widget
    assert_action_performed(widget, "create NumberInput")

    assert not widget.readonly
    assert widget.value is None
    assert widget.step == Decimal("1")
    assert widget.min_value is None
    assert widget.max_value is None
    assert widget._on_change._raw is None


def test_create_with_values():
    "A multiline text input can be created with initial values"
    on_change = Mock()

    widget = toga.NumberInput(
        value=Decimal("2.71828"),
        step=37,
        min_value=-42,
        max_value=420,
        readonly=True,
        on_change=on_change,
    )
    assert widget._impl.interface == widget
    assert_action_performed(widget, "create NumberInput")

    assert widget.readonly
    assert widget.value == Decimal("2.71828")
    assert widget.step == Decimal("37")
    assert widget.min_value == Decimal("-42")
    assert widget.max_value == Decimal("420")
    assert widget._on_change._raw == on_change

    # Change handler hasn't been invoked
    on_change.assert_not_called()


@pytest.mark.parametrize(
    "value, expected",
    [
        # float
        (1.23, Decimal("1.23")),
        (1.23e4, Decimal("12300")),
        # Integer
        (123, Decimal("123")),
        # Float and integer specified as string
        ("1.23", Decimal("1.23")),
        ("123", Decimal("123")),
        ("1.23e+4", Decimal("1.23e+4")),
        # Decimal
        (Decimal("1.23"), Decimal("1.23")),
        # Empty string
        ("", None),
        # None
        (None, None),
    ],
)
def test_value(widget, value, expected):
    "The value of the widget can be set"
    # Clear the event log and validator mock
    EventLog.reset()

    # Define and set a new change callback
    on_change_handler = Mock()
    widget.on_change = on_change_handler

    widget.value = value
    assert widget.value == expected

    # test backend has the right value
    assert attribute_value(widget, "value") == expected

    # A refresh was performed
    assert_action_performed(widget, "refresh")

    # change handler was invoked
    on_change_handler.assert_called_once_with(widget)


@pytest.mark.parametrize(
    "value",
    [
        object(),  # Not convertible
        "Not a number",  # Non-numerical string
    ],
)
def test_bad_value(widget, value):
    "If a value can't be converted into a decimal, an error is raised"
    with pytest.raises(ValueError, match=r"value must be a number or None"):
        widget.value = value


def test_clear(widget):
    """The value of the input can be cleared."""
    # Clear the event log
    EventLog.reset()

    # Define and set a new change callback
    on_change_handler = Mock()
    widget.on_change = on_change_handler

    # Set an initial value on the widget
    widget.value = "1.23"
    assert widget.value == Decimal("1.23")

    # A refresh was performed
    assert_action_performed(widget, "refresh")

    # change handler was invoked
    on_change_handler.assert_called_once_with(widget)

    # Clear the event log and mocks
    EventLog.reset()
    on_change_handler.reset_mock()

    # Clear the widget text.
    widget.clear()
    assert widget.value is None

    # A refresh was performed
    assert_action_performed(widget, "refresh")

    # change handler was invoked
    on_change_handler.assert_called_once_with(widget)


@pytest.mark.parametrize(
    "value, expected",
    [
        # float
        (1.23, Decimal("1.23")),
        (1.23e4, Decimal("12300")),
        # Integer
        (123, Decimal("123")),
        # Float and integer specified as string
        ("1.23", Decimal("1.23")),
        ("123", Decimal("123")),
        ("1.23e+4", Decimal("1.23e+4")),
        # Decimal
        (Decimal("1.23"), Decimal("1.23")),
    ],
)
def test_step(widget, value, expected):
    "The step of the widget can be set"
    widget.step = value
    assert widget.step == expected

    # test backend has the right value
    assert attribute_value(widget, "step") == expected


@pytest.mark.parametrize(
    "value",
    [
        object(),  # Not convertible
        "Not a number",  # Non-numerical string
        "",  # Empty string
        None,
    ],
)
def test_bad_step(widget, value):
    "If a step can't be converted into a decimal, an error is raised"
    with pytest.raises(ValueError, match=r"step must be a number"):
        widget.step = "not a number"


@pytest.mark.parametrize(
    "value, expected",
    [
        # float; approximate because of float conversion
        (1.23, Decimal("1.23")),
        (1.23e4, Decimal("12300")),
        # Integer
        (123, Decimal("123")),
        # Float and integer specified as string
        ("1.23", Decimal("1.23")),
        ("123", Decimal("123")),
        ("1.23e+4", Decimal("1.23e+4")),
        # Decimal
        (Decimal("1.23"), Decimal("1.23")),
        # Empty string
        ("", None),
        # None
        (None, None),
    ],
)
def test_min_value(widget, value, expected):
    "The min_value of the widget can be set"
    widget.min_value = value
    assert widget.min_value == expected

    # test backend has the right value
    assert attribute_value(widget, "min_value") == expected


@pytest.mark.parametrize(
    "value",
    [
        object(),  # Not convertible
        "Not a number",  # Non-numerical string
    ],
)
def test_bad_min_value(widget, value):
    "If a min_value can't be converted into a decimal, an error is raised"
    with pytest.raises(ValueError, match=r"min_value must be a number or None"):
        widget.min_value = value


@pytest.mark.parametrize(
    "value, expected",
    [
        # float
        (1.23, Decimal("1.23")),
        (1.23e4, Decimal("12300")),
        # Integer
        (123, Decimal("123")),
        # Float and integer specified as string
        ("1.23", Decimal("1.23")),
        ("123", Decimal("123")),
        ("1.23e+4", Decimal("1.23e+4")),
        # Decimal
        (Decimal("1.23"), Decimal("1.23")),
        # Empty string
        ("", None),
        # None
        (None, None),
    ],
)
def test_max_value(widget, value, expected):
    "The max_value of the widget can be set"
    widget.max_value = value
    assert widget.max_value == expected

    # test backend has the right value
    assert attribute_value(widget, "max_value") == expected


@pytest.mark.parametrize(
    "value",
    [
        object(),  # Not convertible
        "Not a number",  # Non-numerical string
    ],
)
def test_bad_max_value(widget, value):
    "If a max_value can't be converted into a decimal, an error is raised"
    with pytest.raises(ValueError, match=r"max_value must be a number or None"):
        widget.max_value = value


@pytest.mark.parametrize(
    "provided, clipped",
    [
        (15, Decimal(15)),
        (25, Decimal(20)),
        (5, Decimal(10)),
        (None, None),
    ],
)
def test_clip_on_value_change(widget, provided, clipped):
    "A widget's value will be clipped inside the min/max range."
    widget.min_value = 10
    widget.max_value = 20

    widget.value = provided
    assert widget.value == clipped


@pytest.mark.parametrize(
    "provided, clipped",
    [
        (15, Decimal(15)),
        (25, None),
        (5, None),
        (None, None),
    ],
)
def test_clip_on_retrieval(widget, provided, clipped):
    "A widget's value will be clipped if the widget has a value outside the min/max range."
    widget.min_value = 10
    widget.max_value = 20

    # Inject a raw attribute value.
    widget._impl._set_value("value", provided)
    assert widget.value == clipped


@pytest.mark.parametrize(
    "value, new_max, clipped",
    [
        (10, 15, Decimal(10)),
        (10, 5, Decimal(5)),
        (10, None, Decimal(10)),
        (None, None, None),
        (None, 5, None),
    ],
)
def test_clip_on_max_change(widget, value, new_max, clipped):
    "A widget's value will be clipped if the max value changes"
    # Set an initial max, and a value that is less than it.
    widget.max_value = 20
    widget.value = value

    # Set a new max
    widget.max_value = new_max
    # Value might be clipped
    assert widget.value == clipped


@pytest.mark.parametrize(
    "value, new_min, clipped",
    [
        (20, 15, Decimal(20)),
        (20, 25, Decimal(25)),
        (20, None, Decimal(20)),
        (None, None, None),
        (None, 25, None),
    ],
)
def test_clip_on_min_change(widget, value, new_min, clipped):
    "A widget's value will be clipped if the min value changes"
    # Set an initial max, and a value that is less than it.
    widget.min_value = 10
    widget.value = value

    # Set a new max
    widget.min_value = new_min
    # Value might be clipped
    assert widget.value == clipped


def test_on_change(widget):
    """The on_change handler can be invoked."""
    # No handler initially
    assert widget._on_change._raw is None

    # Define and set a new callback
    handler = Mock()

    widget.on_change = handler

    assert widget.on_change._raw == handler

    # Invoke the callback
    widget._impl.simulate_change()

    # Callback was invoked
    handler.assert_called_once_with(widget)


@pytest.mark.parametrize(
    "value, clean",
    [
        # Valid values
        ("", ""),
        ("123", "123"),
        ("-123", "-123"),
        ("1.23", "1.23"),
        ("-1.23", "-1.23"),
        (".123", ".123"),
        # Non alphanumeric
        ("12a3b", "123"),
        ("12!3@", "123"),
        # - not at the start
        ("1-23", "123"),
        ("123-", "123"),
        ("1.2-3", "1.23"),
        # Multiple . characters
        ("1.2.3", "1.23"),
        ("1..23", "1.23"),
        ("1.23.", "1.23"),
        ("-1.2.3", "-1.23"),
        ("-1..23", "-1.23"),
        ("-1.23.", "-1.23"),
        # Multiple problems
        ("A12.3!4.-56", "12.3456"),
    ],
)
def test_clean_decimal_str(value, clean):
    assert _clean_decimal_str(value) == clean
