from unittest.mock import Mock

import pytest

import toga
from toga_dummy.utils import (
    EventLog,
    assert_action_not_performed,
    assert_action_performed,
    assert_action_performed_with,
    attribute_value,
)
from toga_dummy.widgets.mapview import MapView as DummyMapView


@pytest.fixture
def pin_1():
    return toga.MapPin(toga.LatLng(10.0, 10.0), title="First", subtitle="thing")


@pytest.fixture
def pins(pin_1):
    return [
        pin_1,
        toga.MapPin((20.0, 20.0), title="Second"),
    ]


@pytest.fixture
def widget(pins):
    return toga.MapView(pins=pins)


def test_widget_created(widget):
    "A MapView can be created with minimal arguments"
    widget = toga.MapView()

    assert widget._impl.interface == widget
    assert_action_performed(widget, "create MapView")

    assert widget.location == toga.LatLng(-31.9559, 115.8606)
    assert widget.zoom == 11
    assert set(widget.pins) == set()
    assert repr(widget.pins) == "<MapPinSet (0 pins)>"
    assert widget._on_select._raw is None


def test_create_with_values(pins):
    """A MapView can be created with all available arguments"""
    on_select = Mock()

    widget = toga.MapView(location=(37.0, 42.0), zoom=4, pins=pins, on_select=on_select)

    assert widget._impl.interface == widget
    assert_action_performed(widget, "create MapView")

    assert widget.location == toga.LatLng(37.0, 42.0)
    assert widget.zoom == 4
    assert set(widget.pins) == set(pins)
    assert repr(widget.pins) == "<MapPinSet (2 pins)>"
    assert widget._on_select._raw == on_select


def test_latlng_properties():
    """LatLng objects behave like tuples."""
    # Create a LatLng object.
    pos = toga.LatLng(37.42, 42.37123456)

    # String representation is clean, and clipped to 6dp
    assert str(pos) == "(37.420000, 42.371235)"

    # Values can be accessed by attribute
    assert pos.lat == pytest.approx(37.42)
    assert pos.lng == pytest.approx(42.37123456)

    # Values can be accessed by position
    assert pos[0] == pytest.approx(37.42)
    assert pos[1] == pytest.approx(42.37123456)

    # LatLng can be compared with tuples
    assert pos == pytest.approx((37.42, 42.37123456))


@pytest.mark.parametrize(
    "title, subtitle, value",
    [
        ("The Title", None, "<MapPin @ (37.420000, 42.370000); The Title>"),
        (
            "The Title",
            "The Subtitle",
            "<MapPin @ (37.420000, 42.370000); The Title - The Subtitle>",
        ),
    ],
)
def test_pin_repr(title, subtitle, value):
    """The repr of a pin adapts to the properties that the pin has"""
    pin = toga.MapPin((37.42, 42.37), title=title, subtitle=subtitle)
    assert repr(pin) == value


def test_pin_location(widget):
    """Map pin location can be set and changed."""

    pin = toga.MapPin((37.42, 42.37), title="TheTitle", subtitle="TheSubtitle")

    assert isinstance(pin.location, toga.LatLng)
    assert pin.location == (37.42, 42.37)

    # Change the pin location before the pin is on the map
    EventLog.reset()

    # Pin Location can be changed with a tuple
    pin.location = (23.45, 67.89)
    assert isinstance(pin.location, toga.LatLng)
    assert pin.location == (23.45, 67.89)
    assert_action_not_performed(widget, "update pin")

    # Pin Location can be changed with a LatLng
    pin.location = toga.LatLng(12.34, 56.78)
    assert isinstance(pin.location, toga.LatLng)
    assert pin.location == (12.34, 56.78)
    assert_action_not_performed(widget, "update pin")

    # Add the pin to a map
    widget.pins.add(pin)
    assert_action_performed_with(widget, "add pin", pin=pin)

    # Pin Location can be changed while on the map
    pin.location = (23.45, 67.89)
    assert isinstance(pin.location, toga.LatLng)
    assert pin.location == (23.45, 67.89)
    assert_action_performed_with(widget, "update pin", pin=pin)

    # Remove the pin from the map
    EventLog.reset()
    widget.pins.remove(pin)
    assert_action_performed_with(widget, "remove pin", pin=pin)

    # Updating the location doesn't modify the map
    pin.location = toga.LatLng(12.34, 56.78)
    assert isinstance(pin.location, toga.LatLng)
    assert pin.location == (12.34, 56.78)
    assert_action_not_performed(widget, "update pin")


def test_pin_title(widget):
    """Map pin title can be set and changed."""
    pin = toga.MapPin((37.42, 42.37), title="The Title", subtitle="The Subtitle")
    assert pin.title == "The Title"

    # Change the pin title before the pin is on the map
    EventLog.reset()

    # Pin title can be changed to a string
    pin.title = "New Title"
    assert pin.title == "New Title"
    assert_action_not_performed(widget, "update pin")

    # If a non-string object is used, it is converted to a string
    pin.title = 12345
    assert pin.title == "12345"
    assert_action_not_performed(widget, "update pin")

    # Add the pin to a map
    widget.pins.add(pin)
    assert_action_performed_with(widget, "add pin", pin=pin)

    # Pin title can be changed while on the map
    pin.title = "On map"
    assert pin.title == "On map"
    assert_action_performed_with(widget, "update pin", pin=pin)

    # Remove the pin from the map
    EventLog.reset()
    widget.pins.remove(pin)
    assert_action_performed_with(widget, "remove pin", pin=pin)

    # Updating the title doesn't modify the map
    pin.title = "Off map"
    assert pin.title == "Off map"
    assert_action_not_performed(widget, "update pin")


def test_pin_subtitle(widget):
    """Map pin subtitle can be set and changed."""
    pin = toga.MapPin((37.42, 42.37), title="The Title", subtitle="The Subtitle")
    assert pin.subtitle == "The Subtitle"

    # Change the pin subtitle before the pin is on the map
    EventLog.reset()

    # Pin subtitle can be changed to a string
    pin.subtitle = "New Subtitle"
    assert pin.subtitle == "New Subtitle"
    assert_action_not_performed(widget, "update pin")

    # Pin subtitle can be set to None
    pin.subtitle = None
    assert pin.subtitle is None
    assert_action_not_performed(widget, "update pin")

    # If a non-string object is used, it is converted to a string
    pin.subtitle = 12345
    assert pin.subtitle == "12345"
    assert_action_not_performed(widget, "update pin")

    # Add the pin to a map
    widget.pins.add(pin)
    assert_action_performed_with(widget, "add pin", pin=pin)

    # Pin subtitle can be changed while on the map
    pin.subtitle = "On map"
    assert pin.subtitle == "On map"
    assert_action_performed_with(widget, "update pin", pin=pin)

    # Remove the pin from the map
    EventLog.reset()
    widget.pins.remove(pin)
    assert_action_performed_with(widget, "remove pin", pin=pin)

    # Updating the subtitle doesn't modify the map
    pin.subtitle = "Off map"
    assert pin.subtitle == "Off map"
    assert_action_not_performed(widget, "update pin")


def test_map_location(widget):
    """The map location can be changed."""

    # Location can be set with a tuple
    widget.location = (12.34, 56.78)

    assert isinstance(widget.location, toga.LatLng)
    assert widget.location == toga.LatLng(12.34, 56.78)

    # Location can be set with a LatLng
    widget.location = toga.LatLng(23.45, 67.89)

    assert isinstance(widget.location, toga.LatLng)
    assert widget.location == toga.LatLng(23.45, 67.89)


@pytest.mark.parametrize(
    "value, effective",
    [
        (-5, 0),  # Clipped to minimum
        (0, 0),  # minimum value
        (9, 9),  # mid range value
        (20, 20),  # maximum value
        (25, 20),  # clipped to maximum
        (3.14159, 3),  # converted to integer
        ("4", 4),  # converted to integer
    ],
)
def test_set_zoom(widget, value, effective):
    """Zoom value for the map can be set."""
    EventLog.reset()

    widget.zoom = value
    assert attribute_value(widget, "zoom") == effective
    # round trip the value
    assert widget.zoom == effective


@pytest.mark.parametrize(
    "value, exception",
    [
        (None, TypeError),
        ("a", ValueError),
    ],
)
def test_bad_zoom(widget, value, exception):
    """Bad values for zoom raise an error."""
    with pytest.raises(exception):
        widget.zoom = value


def test_add_remove_pin(widget):
    """Pins can be added and removed from the map."""
    pin = toga.MapPin((37.42, 42.37), title="The Title", subtitle="The Subtitle")

    # Initially 2 pins
    assert len(widget.pins) == 2

    # Add a pin
    widget.pins.add(pin)
    assert_action_performed_with(widget, "add pin", pin=pin)

    # There's now 3 pins
    assert len(widget.pins) == 3

    # Remove a pin
    widget.pins.remove(pin)
    assert_action_performed_with(widget, "remove pin", pin=pin)

    # There's now 2 pins
    assert len(widget.pins) == 2

    # Clear all pins
    widget.pins.clear()

    # There's now 0 pins
    assert len(widget.pins) == 0


def test_select_pin(widget, pin_1):
    """A pin on a map generates an event if selected."""
    # Set up a load handler
    on_select_handler = Mock()
    widget.on_select = on_select_handler

    # The load handler hasn't been called yet
    on_select_handler.assert_not_called()

    # Simulate a pin being selected
    widget._impl.simulate_pin_selected(pin_1)

    # handler has been invoked
    on_select_handler.assert_called_once_with(widget, pin=pin_1)


def test_disabled_on_select(widget):
    """If the backend doesn't support on_select, a warning is raised."""
    try:
        # Temporarily set the feature attribute on the backend
        DummyMapView.SUPPORTS_ON_SELECT = False

        # Instantiate a new widget with a hobbled backend.
        widget = toga.MapView()
        handler = Mock()

        # Setting the handler raises a warning
        with pytest.warns(
            toga.NotImplementedWarning,
            match=r"\[Dummy\] Not implemented: MapView\.on_select",
        ):
            widget.on_select = handler

        # But the handler is still installed
        assert widget.on_select._raw == handler
    finally:
        # Clear the feature attribute.
        del DummyMapView.SUPPORTS_ON_SELECT
