import pytest

import toga
from toga.colors import REBECCAPURPLE
from toga.fonts import FANTASY
from toga.style.pack import HIDDEN, RIGHT, VISIBLE
from toga_dummy.utils import assert_action_performed_with


# Create the simplest possible widget with a concrete implementation that will
# allow children
class ExampleWidget(toga.Widget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._impl = self.factory.Widget(self)
        self._children = []


# Create the simplest possible widget with a concrete implementation that cannot
# have children.
class ExampleLeafWidget(toga.Widget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._impl = self.factory.Widget(self)


@pytest.fixture
def grandchild():
    return ExampleLeafWidget(id="grandchild_id")


@pytest.fixture
def child(grandchild):
    child = ExampleWidget(id="child_id")
    child.add(grandchild)

    return child


@pytest.fixture
def widget(child):
    widget = ExampleWidget(id="widget_id")
    widget.add(child)

    return widget


def test_refresh(widget):
    """Refresh requests are passed to the widget."""
    widget.applicator.refresh()

    assert_action_performed_with(widget, "refresh")


def test_set_bounds(widget, child, grandchild):
    """Bounds changes are passed to all widgets in the tree."""
    # Manually set location of the parent
    widget.layout._origin_left = 100
    widget.layout._origin_top = 200
    widget.layout.content_width = 300
    widget.layout.content_height = 400

    # Manually set location of the child
    child.layout._origin_left = 10
    child.layout._origin_top = 20
    child.layout.content_width = 30
    child.layout.content_height = 40

    # Manually set location of the grandchild
    grandchild.layout._origin_left = 1
    grandchild.layout._origin_top = 2
    grandchild.layout.content_width = 3
    grandchild.layout.content_height = 4

    # Propagate the bounds
    widget.applicator.set_bounds()

    assert_action_performed_with(
        widget, "set bounds", x=100, y=200, width=300, height=400
    )
    assert_action_performed_with(child, "set bounds", x=10, y=20, width=30, height=40)
    assert_action_performed_with(grandchild, "set bounds", x=1, y=2, width=3, height=4)


def test_text_alignment(widget):
    """Text alignment can be set on a widget."""
    widget.applicator.set_text_alignment(RIGHT)

    assert_action_performed_with(widget, "set alignment", alignment=RIGHT)


@pytest.mark.parametrize(
    "child_visibility, grandchild_visibility, value, "
    "widget_hidden, child_hidden, grandchild_hidden",
    [
        # Set widget hidden. All widgets are always hidden,
        # no matter the actual style setting.
        (VISIBLE, VISIBLE, True, True, True, True),
        (VISIBLE, HIDDEN, True, True, True, True),
        (HIDDEN, VISIBLE, True, True, True, True),
        (HIDDEN, HIDDEN, True, True, True, True),
        # Set widget visible. Visibility only cascades
        # as far as the first HIDDEN widget
        (VISIBLE, VISIBLE, False, False, False, False),
        (VISIBLE, HIDDEN, False, False, False, True),
        (HIDDEN, VISIBLE, False, False, True, True),
        (HIDDEN, HIDDEN, False, False, True, True),
    ],
)
def test_set_hidden(
    widget,
    child,
    grandchild,
    child_visibility,
    grandchild_visibility,
    value,
    widget_hidden,
    child_hidden,
    grandchild_hidden,
):
    """Widget visibility can be controlled, and is transitive into children."""
    # Set the explicit visibility of the child and grandchild
    child.style.visibility = child_visibility
    grandchild.style.visibility = grandchild_visibility

    # Set widget visibility
    widget.applicator.set_hidden(value)

    assert_action_performed_with(widget, "set hidden", hidden=widget_hidden)
    assert_action_performed_with(child, "set hidden", hidden=child_hidden)
    assert_action_performed_with(grandchild, "set hidden", hidden=grandchild_hidden)

    # The style property of the child and grandchild hasn't changed.
    assert child.style.visibility == child_visibility
    assert grandchild.style.visibility == grandchild_visibility


def test_set_font(widget):
    """A font change can be applied to a widget."""
    widget.applicator.set_font(FANTASY)

    assert_action_performed_with(widget, "set font", font=FANTASY)


def test_set_color(widget):
    """A color change can be applied to a widget."""
    widget.applicator.set_color(REBECCAPURPLE)

    assert_action_performed_with(widget, "set color", color=REBECCAPURPLE)


def test_set_background_color(child, widget):
    """A background color change can be applied to a widget."""
    widget.applicator.set_background_color(REBECCAPURPLE)

    assert_action_performed_with(widget, "set background color", color=REBECCAPURPLE)
