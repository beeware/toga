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
    # The impl-level add-child will not be called,
    # because the box hasn't been assigned to a window
    assert_action_not_performed(box, "add child")

    # But the box will have children.
    assert box.children == [child1, child2]
