import pytest

import toga
from toga.colors import BLACK, BLUE, GREEN, RED
from toga.style import Pack
from toga.style.pack import HIDDEN, VISIBLE

from .probe import get_probe


@pytest.fixture
async def widget():
    return toga.Box(style=Pack(width=100, height=200, background_color=RED))


async def test_visibility(widget, probe):
    "A widget (and it's children) can be made invisible"
    child = toga.Box(style=Pack(width=75, height=100, background_color=GREEN))
    child_probe = get_probe(child)

    grandchild = toga.Button("Hello")
    grandchild_probe = get_probe(grandchild)
    child.add(grandchild)

    other = toga.Box(style=Pack(width=100, height=200, background_color=BLUE))
    other_probe = get_probe(other)

    widget.parent.add(other)
    widget.add(child)

    await probe.redraw("Widget should be visible")

    # Widgets are all visible an in place
    assert not probe.is_hidden
    assert not child_probe.is_hidden
    assert not grandchild_probe.is_hidden
    probe.assert_layout(position=(0, 0), size=(100, 200))
    other_probe.assert_layout(position=(100, 0), size=(100, 200))

    # Hide the widget
    widget.style.visibility = HIDDEN
    await probe.redraw("Widget should be hidden")

    # Widgets are no longer visible.
    assert probe.is_hidden
    assert child_probe.is_hidden
    assert grandchild_probe.is_hidden
    # Making the widget invisible doesn't affect layout
    probe.assert_layout(position=(0, 0), size=(100, 200))
    other_probe.assert_layout(position=(100, 0), size=(100, 200))

    # Make widget visible again
    widget.style.visibility = VISIBLE
    await probe.redraw("Widget should be visible again")

    # Widgets are all visible and in place again.
    assert not probe.is_hidden
    assert not child_probe.is_hidden
    assert not grandchild_probe.is_hidden
    probe.assert_layout(position=(0, 0), size=(100, 200))
    other_probe.assert_layout(position=(100, 0), size=(100, 200))

    # Hide the widget again
    widget.style.visibility = HIDDEN
    await probe.redraw("Widget should be hidden again")

    # Widgets are no longer visible.
    assert probe.is_hidden
    assert child_probe.is_hidden
    assert grandchild_probe.is_hidden

    # Mark the child style as visible.
    child.style.visibility = VISIBLE
    await probe.redraw("Child style of widget should be visible")

    # Root widget isn't visible, so neither descendent is visible.
    assert probe.is_hidden
    assert child_probe.is_hidden
    assert grandchild_probe.is_hidden

    # Explicitly mark the child style as hidden.
    child.style.visibility = HIDDEN
    await probe.redraw("Child style of widget should be hidden")

    # Root widget isn't visible, so neither descendent is visible.
    assert probe.is_hidden
    assert child_probe.is_hidden
    assert grandchild_probe.is_hidden

    # Mark the root widget as visible again.
    widget.style.visibility = VISIBLE
    await probe.redraw("Child style of widget should be visible again")

    # Root widget is visible again but the child is explicitly hidden,
    # so it and the grandchild are still hidden
    assert not probe.is_hidden
    assert child_probe.is_hidden
    assert grandchild_probe.is_hidden


async def test_parenting(widget, probe):
    "A widget can be reparented between containers"
    box = widget.parent

    child = toga.Box(style=Pack(width=50, height=75, background_color=GREEN))
    child_probe = get_probe(child)
    other = toga.Box(style=Pack(width=100, height=200, background_color=BLUE))
    other_probe = get_probe(other)
    other_child = toga.Box(style=Pack(width=25, height=50, background_color=BLACK))
    other.add(other_child)

    # Layout has the test widget, plus other, horizontally laid out.
    # Child isn't in the layout yet.
    box.add(other)
    await probe.redraw("Child should not in layout yet")
    probe.assert_layout(position=(0, 0), size=(100, 200))
    other_probe.assert_layout(position=(100, 0), size=(100, 200))
    child_probe.assert_not_contained()

    # Add child to widget.
    widget.add(child)
    await probe.redraw("Child should be added to layout")
    probe.assert_layout(position=(0, 0), size=(100, 200))
    other_probe.assert_layout(position=(100, 0), size=(100, 200))
    child_probe.assert_layout(position=(0, 0), size=(50, 75))

    # Re-add child to the *same* widget
    widget.add(child)
    await probe.redraw("Child should be re-added to the same widget")
    probe.assert_layout(position=(0, 0), size=(100, 200))
    other_probe.assert_layout(position=(100, 0), size=(100, 200))
    child_probe.assert_layout(position=(0, 0), size=(50, 75))

    # Reparent child to other without removing first
    other.add(child)
    await probe.redraw(
        message="Child should be reparent to other without removing first"
    )
    probe.assert_layout(position=(0, 0), size=(100, 200))
    other_probe.assert_layout(position=(100, 0), size=(100, 200))
    child_probe.assert_layout(position=(125, 0), size=(50, 75))

    # Remove child from the layout entirely
    other.remove(child)
    await probe.redraw("Child should be removed from the layout entirely")
    probe.assert_layout(position=(0, 0), size=(100, 200))
    other_probe.assert_layout(position=(100, 0), size=(100, 200))
    child_probe.assert_not_contained()

    # Insert the child into the root layout
    box.insert(1, child)
    await probe.redraw("Child should be inserted to the root layout")
    probe.assert_layout(position=(0, 0), size=(100, 200))
    other_probe.assert_layout(position=(150, 0), size=(100, 200))
    child_probe.assert_layout(position=(100, 0), size=(50, 75))


async def test_tab_index(widget, probe, other):
    if toga.platform.current_platform not in {"windows"}:
        assert widget.tab_index is None
        assert other.tab_index is None
    else:
        assert widget.tab_index == 1
        assert other.tab_index == 2

        widget.tab_index = 4
        other.tab_index = 2
        assert widget.tab_index == 4
        assert other.tab_index == 2
