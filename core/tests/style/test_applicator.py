import pytest

import toga
from toga.colors import REBECCAPURPLE
from toga.fonts import FANTASY
from toga.style.pack import RIGHT, VISIBLE
from toga_dummy.utils import assert_action_performed_with


# Create the simplest possible widget with a concrete implementation that will
# allow children
class TestWidget(toga.Widget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._impl = self.factory.Widget(self)
        self._children = []


# Create the simplest possible widget with a concrete implementation that cannot
# have children.
class TestLeafWidget(toga.Widget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._impl = self.factory.Widget(self)


@pytest.fixture
def child():
    return TestLeafWidget(id="child_id")


@pytest.fixture
def widget(child):
    widget = TestWidget(id="widget_id")
    widget.add(child)

    return widget


def test_refresh(widget):
    "Refresh requests are passed to the widget"
    widget.applicator.refresh()

    assert_action_performed_with(widget, "refresh")


def test_set_bounds(child, widget):
    "Bounds changes are passed to all widgets in the tree"
    # Manually set location of the parent
    widget.layout._origin_left = 10
    widget.layout._origin_top = 20
    widget.layout.content_width = 30
    widget.layout.content_height = 40

    # Manually set location of the child
    child.layout._origin_left = 1
    child.layout._origin_top = 2
    child.layout.content_width = 3
    child.layout.content_height = 4

    # Propegate the boundsq
    widget.applicator.set_bounds()

    assert_action_performed_with(widget, "set bounds", x=10, y=20, width=30, height=40)
    assert_action_performed_with(child, "set bounds", x=1, y=2, width=3, height=4)


def test_text_alignment(widget):
    "Text alignment can be set on a widget"
    widget.applicator.set_text_alignment(RIGHT)

    assert_action_performed_with(widget, "set alignment", alignment=RIGHT)


def test_set_hidden(widget, child):
    "Visibility can be set on a widget"
    widget.applicator.set_hidden(True)

    assert_action_performed_with(widget, "set hidden", hidden=True)
    # The hide is applied transitively to the child
    assert_action_performed_with(child, "set hidden", hidden=True)
    # However, the style property of the child hasn't changed.
    assert child.style.visibility == VISIBLE


def test_set_font(widget):
    "A font change can be applied to a widget"
    widget.applicator.set_font(FANTASY)

    assert_action_performed_with(widget, "set font", font=FANTASY)


def test_set_color(widget):
    "A color change can be applied to a widget"
    widget.applicator.set_color(REBECCAPURPLE)

    assert_action_performed_with(widget, "set color", color=REBECCAPURPLE)


def test_set_background_color(child, widget):
    "A background color change can be applied to a widget"
    widget.applicator.set_background_color(REBECCAPURPLE)

    assert_action_performed_with(widget, "set background color", color=REBECCAPURPLE)
