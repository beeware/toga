import pytest

import toga
from toga.style import Pack
from toga_dummy.utils import (
    assert_action_not_performed,
    assert_action_performed,
    assert_action_performed_with,
)


def test_create_box():
    """A Box can be created."""
    box = toga.Box()
    # Round trip the impl/interface
    assert box._impl.interface == box

    assert_action_performed(box, "create Box")
    assert_action_not_performed(box, "add child")


def test_create_box_with_children():
    """A Box can be created with children."""
    child1 = toga.Box()
    child2 = toga.Box()
    box = toga.Box(
        id="foobar",
        children=[child1, child2],
        # A style property
        width=256,
    )

    # Round trip the impl/interface
    assert box._impl.interface == box

    assert_action_performed(box, "create Box")
    assert_action_performed_with(box, "add child", child=child1._impl)
    assert_action_performed_with(box, "add child", child=child2._impl)

    # But the box will have children.
    assert box.children == [child1, child2]

    # Other properties are preserved
    assert box.id == "foobar"
    assert box.style.width == 256


def test_disable_no_op():
    """Box doesn't have a disabled state."""
    box = toga.Box()

    # Enabled by default
    assert box.enabled

    # Try to disable the widget
    box.enabled = False

    # Still enabled.
    assert box.enabled


def test_focus_noop():
    """Focus is a no-op."""
    box = toga.Box()

    box.focus()
    assert_action_not_performed(box, "focus")


@pytest.mark.parametrize("direction", ["row", "column"])
def test_row_column(direction):
    """Row and Column shorthands can be used."""
    func = getattr(toga, direction.capitalize())
    box = func(
        id="my-id",  # Non-style property
        width=100,  # Style property
        style=Pack(height=200),  # Style object
    )
    assert type(box) is toga.Box
    assert box.id == "my-id"
    assert box.style.direction == direction
    assert box.style.width == 100
    assert box.style.height == 200


@pytest.mark.parametrize("func_direction", ["column", "row"])
@pytest.mark.parametrize("style_direction", ["column", "row"])
def test_row_column_conflict_style(func_direction, style_direction):
    """If a shorthand function is passed a style object specifying a direction,
    the shorthand takes priority, and the style object is not modified."""
    func = getattr(toga, func_direction.capitalize())
    style = Pack(direction=style_direction)
    box = func(style=style)
    assert box.style.direction == func_direction
    assert style.direction == style_direction


@pytest.mark.parametrize("func_direction", ["column", "row"])
@pytest.mark.parametrize("mixin_direction", ["column", "row"])
def test_row_column_conflict_mixin(func_direction, mixin_direction):
    """If a shorthand function is passed a mixin argument specifying a direction,
    an exception is raised."""
    func = getattr(toga, func_direction.capitalize())
    with pytest.raises(
        TypeError, match="got multiple values for keyword argument 'direction'"
    ):
        func(direction=mixin_direction)
