import pytest

import toga
from toga.app import WidgetRegistry


@pytest.fixture
def widget_registry():
    return WidgetRegistry()


# Create the simplest possible widget with a concrete implementation
class ExampleWidget(toga.Widget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._impl = self.factory.Widget(self)

    def __repr__(self):
        return f"Widget(id={self.id!r})"


def test_empty_registry(widget_registry):
    assert len(widget_registry) == 0
    assert list(widget_registry) == []
    assert str(widget_registry) == "{}"


def test_add_widget(widget_registry):
    """Widgets can be added to the registry."""
    # Add a widget to the registry
    widget1 = ExampleWidget(id="widget-1")
    widget_registry._add(widget1)

    assert len(widget_registry) == 1
    assert list(widget_registry) == [widget1]
    assert str(widget_registry) == "{'widget-1': Widget(id='widget-1')}"
    assert widget_registry["widget-1"] == widget1

    # Add a second widget
    widget2 = ExampleWidget(id="widget-2")
    widget_registry._add(widget2)

    assert len(widget_registry) == 2
    assert widget_registry["widget-1"] == widget1
    assert widget_registry["widget-2"] == widget2


def test_update_widgets(widget_registry):
    """The registry can be bulk updated."""
    # Add a widget to the registry
    widget1 = ExampleWidget(id="widget-1")
    widget_registry._add(widget1)

    widget2 = ExampleWidget(id="widget-2")
    widget3 = ExampleWidget(id="widget-3")
    widget4 = ExampleWidget(id="widget-4")
    widget_registry._update({widget2, widget3, widget4})

    assert len(widget_registry) == 4
    assert widget_registry["widget-1"] == widget1
    assert widget_registry["widget-2"] == widget2
    assert widget_registry["widget-3"] == widget3
    assert widget_registry["widget-4"] == widget4


def test_remove_widget(widget_registry):
    """A widget can be removed from the repository."""
    "Widgets can be added to the registry"
    # Add a widget to the registry
    widget1 = ExampleWidget(id="widget-1")
    widget2 = ExampleWidget(id="widget-2")
    widget_registry._update({widget1, widget2})

    assert len(widget_registry) == 2

    widget_registry._remove("widget-2")

    assert widget_registry["widget-1"] == widget1
    assert "widget-2" not in widget_registry


def test_add_same_widget_twice(widget_registry):
    """A widget cannot be added to the same registry twice."""
    # Add a widget to the registry
    widget1 = ExampleWidget(id="widget-1")
    widget_registry._add(widget1)

    assert len(widget_registry) == 1

    # Add the widget again; this raises an error
    with pytest.raises(
        KeyError,
        match=r"There is already a widget with the id 'widget-1'",
    ):
        widget_registry._add(widget1)

    # Widget is still there
    assert len(widget_registry) == 1
    assert widget_registry["widget-1"] == widget1


def test_add_duplicate_id(widget_registry):
    """A widget cannot be added to the same registry twice."""
    # Add a widget to the registry
    widget1 = ExampleWidget(id="widget-1")
    widget_registry._add(widget1)

    assert len(widget_registry) == 1

    new_widget = ExampleWidget(id="widget-1")

    # Add the widget again; this raises an error
    with pytest.raises(
        KeyError,
        match=r"There is already a widget with the id 'widget-1'",
    ):
        widget_registry._add(new_widget)

    # Widget is still there
    assert len(widget_registry) == 1
    assert widget_registry["widget-1"] == widget1


def test_setitem(widget_registry):
    """Widgets cannot be directly assigned to the registry."""
    widget1 = ExampleWidget(id="widget-1")

    with pytest.raises(
        TypeError,
        match=r"'WidgetRegistry' object does not support item assignment",
    ):
        widget_registry["new is"] = widget1
