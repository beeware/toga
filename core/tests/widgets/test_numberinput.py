from decimal import Decimal
from unittest.mock import Mock

import pytest

import toga
from toga.widgets.numberinput import _clean_decimal, _clean_decimal_str
from toga_dummy.utils import (
    EventLog,
    assert_action_performed,
    attribute_value,
)


@pytest.fixture
def widget():
    return toga.NumberInput(step="0.01")


def test_widget_created():
    """A NumberInput can be created with minimal arguments."""
    widget = toga.NumberInput()

    assert widget._impl.interface == widget
    assert_action_performed(widget, "create NumberInput")

    assert not widget.readonly
    assert widget.value is None
    assert widget.step == Decimal("1")
    assert widget.min is None
    assert widget.max is None
    assert widget._on_change._raw is None


def test_create_with_values():
    """A NumberInput can be created with initial values."""
    on_change = Mock()

    widget = toga.NumberInput(
        value=Decimal("2.71828"),
        step=0.001,
        min=-42,
        max=420,
        readonly=True,
        on_change=on_change,
    )
    assert widget._impl.interface == widget
    assert_action_performed(widget, "create NumberInput")

    assert widget.readonly
    assert widget.value == Decimal("2.718")
    assert widget.step == Decimal("0.001")
    assert widget.min == Decimal("-42")
    assert widget.max == Decimal("420")
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
        # Excessive precision is rounded to same number of decimal places as step
        # (see QUANTIZE_PARAMS for related tests).
        ("1.23456", Decimal("1.23")),
        ("1.235", Decimal("1.24")),
        # Decimal
        (Decimal("1.23"), Decimal("1.23")),
        # Empty string
        ("", None),
        # None
        (None, None),
    ],
)
def test_value(widget, value, expected):
    """The value of the widget can be set."""
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
    """If a value can't be converted into a decimal, an error is raised."""
    with pytest.raises(ValueError, match=r"value must be a number or None"):
        widget.value = value


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
    """The step of the widget can be set."""
    widget.step = value
    assert widget.step == expected

    # test backend has the right value
    assert attribute_value(widget, "step") == expected


QUANTIZE_PARAMS = (
    "step, expected",
    [
        ("0.0001", Decimal("12.3456")),
        ("0.001", Decimal("12.346")),
        ("0.009", Decimal("12.346")),
        ("0.010", Decimal("12.346")),
        ("0.01", Decimal("12.35")),
        ("0.1", Decimal("12.3")),
        ("1", Decimal("12")),
        ("10", Decimal("12")),
    ],
)


@pytest.mark.parametrize(*QUANTIZE_PARAMS)
def test_quantization(widget, step, expected):
    """The value is quantized to the precision of the step."""
    widget.step = step
    widget.value = 12.3456

    # The value has been quantized to the step
    assert widget.value == expected


@pytest.mark.parametrize(*QUANTIZE_PARAMS)
def test_quantize_on_retrieval(widget, step, expected):
    """A widget's value will be quantized on retrieval."""
    widget.step = step

    # Inject a raw attribute value.
    widget._impl._set_value("value", 12.3456)
    assert widget.value == expected


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
    """If a step can't be converted into a decimal, an error is raised."""
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
        # Integer (but a value that evaluates as false)
        (0, Decimal("0")),
        # Float and integer specified as string
        ("1.23", Decimal("1.23")),
        ("123", Decimal("123")),
        ("1.23e+4", Decimal("1.23e+4")),
        # Excessive precision is truncated to step value
        ("1.23456", Decimal("1.23")),
        # Decimal
        (Decimal("1.23"), Decimal("1.23")),
        # Empty string
        ("", None),
        # None
        (None, None),
    ],
)
def test_min(widget, value, expected):
    """The min of the widget can be set."""
    widget.min = value
    assert widget.min == expected

    # test backend has the right value
    assert attribute_value(widget, "min") == expected


@pytest.mark.parametrize(
    "value",
    [
        object(),  # Not convertible
        "Not a number",  # Non-numerical string
    ],
)
def test_bad_min(widget, value):
    """If a min can't be converted into a decimal, an error is raised."""
    with pytest.raises(ValueError, match=r"min must be a number or None"):
        widget.min = value


def test_min_greater_than_max(widget):
    """If the new min value exceeds the max value, the max value is clipped."""
    widget.max = 10
    widget.min = 100

    assert widget.max == 100
    assert widget.min == 100


@pytest.mark.parametrize(*QUANTIZE_PARAMS)
def test_min_quantized(widget, step, expected):
    """An existing min value is re-quantized after a change in step."""
    # Set a small step so that the min value isn't quantized
    widget.step = 0.00000001
    widget.min = 12.3456

    # Set a new minimum
    widget.step = step

    # The minimum has been re-quantized
    assert widget.min == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        # float
        (1.23, Decimal("1.23")),
        (1.23e4, Decimal("12300")),
        # Integer
        (123, Decimal("123")),
        # Integer (but a value that evaluates as false)
        (0, Decimal("0")),
        # Float and integer specified as string
        ("1.23", Decimal("1.23")),
        ("123", Decimal("123")),
        ("1.23e+4", Decimal("1.23e+4")),
        # Excessive precision is truncated to step value
        ("1.23456", Decimal("1.23")),
        # Decimal
        (Decimal("1.23"), Decimal("1.23")),
        # Empty string
        ("", None),
        # None
        (None, None),
    ],
)
def test_max(widget, value, expected):
    """The max of the widget can be set."""
    widget.max = value
    assert widget.max == expected

    # test backend has the right value
    assert attribute_value(widget, "max") == expected


@pytest.mark.parametrize(
    "value",
    [
        object(),  # Not convertible
        "Not a number",  # Non-numerical string
    ],
)
def test_bad_max(widget, value):
    """If a max can't be converted into a decimal, an error is raised."""
    with pytest.raises(ValueError, match=r"max must be a number or None"):
        widget.max = value


def test_max_less_than_min(widget):
    """If the new max value is less than the min value, the min value is clipped."""
    widget.min = 100
    widget.max = 10

    assert widget.max == 10
    assert widget.min == 10


@pytest.mark.parametrize(*QUANTIZE_PARAMS)
def test_max_quantized(widget, step, expected):
    """An existing max value is re-quantized after a change in step."""
    # Set a small step so that the max value isn't quantized
    widget.step = 0.00000001
    widget.max = 12.3456

    # Set a new maximum
    widget.step = step

    # The maximum has been re-quantized
    assert widget.max == expected


@pytest.mark.parametrize(
    "min, max, provided, clipped",
    [
        (10, 20, 15, Decimal(15)),
        (10, 20, 25, Decimal(20)),
        (10, 20, 5, Decimal(10)),
        (10, 20, None, None),
        # Check min/max values of 0
        (0, 20, -15, Decimal(0)),
        (-10, 0, 25, Decimal(0)),
    ],
)
def test_clip_on_value_change(widget, min, max, provided, clipped):
    """A widget's value will be clipped inside the min/max range."""
    widget.min = min
    widget.max = max

    widget.value = provided
    assert widget.value == clipped


@pytest.mark.parametrize(
    "min, max, provided, clipped",
    [
        (10, 20, 15, Decimal(15)),
        (10, 20, 25, Decimal(20)),
        (10, 20, 5, Decimal(10)),
        (10, 20, None, None),
        # Check min/max values of 0
        (0, 20, -15, Decimal(0)),
        (-10, 0, 25, Decimal(0)),
        # Check a "raw" value of 0
        (10, 20, 0, Decimal(10)),
        (-20, -10, 0, Decimal(-10)),
    ],
)
def test_clip_on_retrieval(widget, min, max, provided, clipped):
    """A widget's value will be clipped if the widget has a value outside the min/max
    range."""
    widget.min = min
    widget.max = max

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
    """A widget's value will be clipped if the max value changes."""
    # Set an initial max, and a value that is less than it.
    widget.max = 20
    widget.value = value

    # Set a new max
    widget.max = new_max
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
    """A widget's value will be clipped if the min value changes."""
    # Set an initial max, and a value that is less than it.
    widget.min = 10
    widget.value = value

    # Set a new max
    widget.min = new_min
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
        # Non-alphanumeric
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


@pytest.mark.parametrize(
    "value, step, clean",
    [
        # Strings of integers
        ("123", None, "123"),
        ("123", "10", "123"),
        ("123", "0.01", "123.00"),
        # Strings of floats
        ("1.23456", None, "1.23456"),
        ("1.23456", "10", "1"),
        ("1.23456", "0.01", "1.23"),
        # Integers
        (123, None, "123"),
        (123, "10", "123"),
        (123, "0.01", "123.00"),
        # Floats
        (1.23456, None, "1.23456"),
        (1.23456, "10", "1"),
        (1.23456, "0.01", "1.23"),
    ],
)
def test_clean_decimal(value, step, clean):
    assert _clean_decimal(value, Decimal(step) if step else step) == Decimal(clean)


def test_deprecated_names():
    """The deprecated min_value/max_value names still work."""
    # Can't specify min and min_value
    with pytest.raises(
        ValueError,
        match=r"Cannot specify both min and min_value",
    ):
        toga.NumberInput(min=2, min_value=4)

    # Can't specify min and min_value
    with pytest.raises(
        ValueError,
        match=r"Cannot specify both max and max_value",
    ):
        toga.NumberInput(max=2, max_value=4)

    # min_value is deprecated
    with pytest.warns(
        DeprecationWarning,
        match="NumberInput.min_value has been renamed NumberInput.min",
    ):
        widget = toga.NumberInput(min_value=2)

    assert widget.min == 2

    with pytest.warns(
        DeprecationWarning,
        match="NumberInput.min_value has been renamed NumberInput.min",
    ):
        assert widget.min_value == 2

    with pytest.warns(
        DeprecationWarning,
        match="NumberInput.min_value has been renamed NumberInput.min",
    ):
        widget.min_value = 4

    assert widget.min == 4

    # max_value is deprecated
    with pytest.warns(
        DeprecationWarning,
        match="NumberInput.max_value has been renamed NumberInput.max",
    ):
        widget = toga.NumberInput(max_value=2)

    assert widget.max == 2

    with pytest.warns(
        DeprecationWarning,
        match="NumberInput.max_value has been renamed NumberInput.max",
    ):
        assert widget.max_value == 2

    with pytest.warns(
        DeprecationWarning,
        match="NumberInput.max_value has been renamed NumberInput.max",
    ):
        widget.max_value = 4

    assert widget.max == 4
