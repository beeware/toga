import toga
from toga_dummy.utils import (
    assert_action_not_performed,
    assert_action_performed,
)


def test_create_box():
    "A Box can be created."
    box = toga.Box()
    # Round trip the impl/interface
    assert box._impl.interface == box

    assert_action_performed(box, "create Box")
    assert_action_not_performed(box, "add child")


def test_create_box_with_children():
    "A Box can be created with children."
    child1 = toga.Box()
    child2 = toga.Box()
    box = toga.Box(children=[child1, child2])

    # Round trip the impl/interface
    assert box._impl.interface == box

    assert_action_performed(box, "create Box")
    # The box has children, so add child also occurs.
    assert_action_performed(box, "add child")

    # But the box will have children.
    assert box.children == [child1, child2]


def test_disable_no_op():
    "Box doesn't have a disabled state"
    box = toga.Box()

    # Enabled by default
    assert box.enabled

    # Try to disable the widget
    box.enabled = False

    # Still enabled.
    assert box.enabled


def test_focus_noop():
    "Focus is a no-op."
    box = toga.Box()

    box.focus()
    assert_action_not_performed(box, "focus")
