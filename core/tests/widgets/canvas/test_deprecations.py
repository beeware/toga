from weakref import ref

import pytest

import toga
import toga.widgets.canvas as canvas_module
from toga.constants import FillRule
from toga.widgets.canvas import (
    Arc,
    BeginPath,
    BezierCurveTo,
    ClosePath,
    DrawImage,
    DrawingAction,
    Ellipse,
    Fill,
    LineTo,
    MoveTo,
    QuadraticCurveTo,
    Rect,
    ResetTransform,
    Rotate,
    Scale,
    State,
    Stroke,
    Translate,
    WriteText,
)
from toga_dummy.utils import (
    EventLog,
    assert_action_not_performed,
    assert_action_performed,
)

# Insert a dead weakref first in the list, just to make sure we cover the case of
# checking against a nonexistent canvas.
toga.Canvas._instances.insert(0, ref(toga.Canvas()))


@pytest.mark.parametrize(
    "old_name, cls",
    [
        ("DrawingObject", DrawingAction),
        ("Context", State),
        ("FillContext", Fill),
        ("StrokeContext", Stroke),
        ("ClosedPathContext", ClosePath),
    ],
)
def test_deprecated_class_names(old_name, cls):
    """Deprecated names work, but issue a warning."""
    with pytest.warns(
        DeprecationWarning,
        match=rf"{old_name} has been renamed to {cls.__name__}",
    ):
        old_cls = getattr(canvas_module, old_name)

    assert old_cls is cls


def test_invalid_class_name():
    # A completely bogus name still fails.
    with pytest.raises(ImportError):
        from toga.widgets.canvas import Nonexistent  # noqa: F401


def test_renamed_root_state(widget):
    with pytest.deprecated_call():
        context_property = widget.context

    assert context_property is widget.root_state


@pytest.mark.parametrize(
    "method_name, args, DrawingActionClass",
    [
        ("begin_path", (), BeginPath),
        ("close_path", (), ClosePath),
        ("ClosedPath", (), ClosePath),  # Deprecated alias
        ("move_to", (0, 0), MoveTo),
        ("line_to", (0, 0), LineTo),
        ("bezier_curve_to", (0, 0, 0, 0, 0, 0), BezierCurveTo),
        ("quadratic_curve_to", (0, 0, 0, 0), QuadraticCurveTo),
        ("arc", (0, 0, 0), Arc),
        ("ellipse", (0, 0, 0, 0), Ellipse),
        ("rect", (0, 0, 0, 0), Rect),
        ("fill", (), Fill),
        ("Fill", (), Fill),  # Deprecated alias
        ("stroke", (), Stroke),
        ("Stroke", (), Stroke),  # Deprecated alias
        ("write_text", ("",), WriteText),
        ("draw_image", (), DrawImage),
        ("rotate", (0,), Rotate),
        ("scale", (0, 0), Scale),
        ("translate", (0, 0), Translate),
        ("reset_transform", (), ResetTransform),
        ("state", (), State),
        ("Context", (), State),  # Deprecated alias
    ],
)
def test_state_drawing_methods(app, widget, method_name, args, DrawingActionClass):
    """State drawing methods are deprecated, but still work."""
    with widget.state() as state:
        pass

    if DrawingActionClass is DrawImage:
        # Can't create image from path until app fixture is loaded.
        args = (toga.Image("resources/sample.png"),)

    # Add to a state that's neither active nor root, to make sure the actions are going
    # to the right place.
    with pytest.deprecated_call():
        drawing_action = getattr(state, method_name)(*args)

    assert state.drawing_actions == [drawing_action]
    assert isinstance(drawing_action, DrawingActionClass)
    assert_action_performed(widget, "redraw")


def test_state_canvas_reference(widget):
    """Retrieving a widget's state is deprecated."""
    state = widget.root_state

    # Make another canvas, just to be sure we get the right one.
    _ = toga.Canvas()

    with pytest.deprecated_call():
        assert state.canvas == widget


def test_state_redraw(widget):
    """State.redraw() is deprecated, but still works."""
    state = widget.root_state

    # Attach it to a second canvas.
    other = toga.Canvas()
    with pytest.deprecated_call():
        other.root_state.append(state)
    # Clear the redraw from the append
    EventLog.reset()

    # Check a canvas it's *not* attached to as well.
    unrelated = toga.Canvas()

    with pytest.deprecated_call():
        state.redraw()

    assert_action_performed(widget, "redraw")
    assert_action_performed(other, "redraw")
    assert_action_not_performed(unrelated, "redraw")


def test_unattached_state(widget):
    """An unattached state doesn't have a canvas or redraw anything."""
    state = State()

    with pytest.deprecated_call():
        assert state.canvas is None

    with pytest.deprecated_call():
        state.redraw()

    assert_action_not_performed(widget, "redraw")


@pytest.mark.parametrize(
    "method_name, DrawingActionClass",
    [
        ("ClosedPath", ClosePath),
        ("Fill", Fill),
        ("Stroke", Stroke),
        ("Context", State),
    ],
)
def test_deprecated_canvas_methods(widget, method_name, DrawingActionClass):
    """The Canvas CamelCase methods are deprecated, and add to root state."""
    with widget.state() as state:
        # Test within an open sub-state, to verify it adds to root state.
        with pytest.deprecated_call():
            drawing_action = getattr(widget, method_name)()

    assert widget.root_state.drawing_actions == [state, drawing_action]
    assert isinstance(drawing_action, DrawingActionClass)
    assert_action_performed(widget, "redraw")


def test_deprecated_list_methods(widget):
    """The order of state objects can be changed."""

    # Initially nothing on the state.
    with pytest.deprecated_call():
        assert len(widget.root_state) == 0

    # Set up an inner state that has contained operations, including a sub-state
    widget.line_to(0, 0)
    with widget.state() as state:
        widget.line_to(10, 20)
        second = widget.line_to(20, 30)
        with widget.fill() as fill:
            widget.line_to(25, 25)
        widget.line_to(30, 40)
        widget.line_to(40, 50)
    widget.line_to(99, 99)

    # Counts are as expected
    with pytest.deprecated_call():
        assert len(widget.root_state) == 3
    with pytest.deprecated_call():
        assert len(state) == 5
    with pytest.deprecated_call():
        assert len(fill) == 1

    # Initial draw instructions are as expected
    assert widget._impl.draw_instructions == [
        "save",
        ("line to", {"x": 0, "y": 0}),
        "save",
        ("line to", {"x": 10, "y": 20}),
        ("line to", {"x": 20, "y": 30}),
        # Begin fill
        "save",
        "begin path",
        ("line to", {"x": 25, "y": 25}),
        ("fill", {"fill_rule": FillRule.NONZERO}),
        "restore",
        # End fill
        ("line to", {"x": 30, "y": 40}),
        ("line to", {"x": 40, "y": 50}),
        "restore",
        ("line to", {"x": 99, "y": 99}),
        "restore",
    ]

    with pytest.deprecated_call():
        # Remove the second draw instruction
        state.remove(second)
    # Drawing objects are as expected
    with pytest.deprecated_call():
        assert len(widget.root_state) == 3
    for i, cls in enumerate([LineTo, State, LineTo]):
        with pytest.deprecated_call():
            assert isinstance(widget.root_state[i], cls)
    with pytest.deprecated_call():
        with pytest.raises(IndexError):
            widget.root_state[3]

    with pytest.deprecated_call():
        assert len(state) == 4
    with pytest.deprecated_call():
        assert len(fill) == 1

    from pprint import pprint

    pprint(widget._impl.draw_instructions)
    # Draw instructions no longer have the second
    assert widget._impl.draw_instructions == [
        "save",
        ("line to", {"x": 0, "y": 0}),
        "save",
        ("line to", {"x": 10, "y": 20}),
        # Begin fill
        "save",
        "begin path",
        ("line to", {"x": 25, "y": 25}),
        ("fill", {"fill_rule": FillRule.NONZERO}),
        "restore",
        # End fill
        ("line to", {"x": 30, "y": 40}),
        ("line to", {"x": 40, "y": 50}),
        "restore",
        ("line to", {"x": 99, "y": 99}),
        "restore",
    ]

    with pytest.deprecated_call():
        # Insert the second draw instruction at index 3
        state.insert(3, second)

    # Counts are as expected
    with pytest.deprecated_call():
        assert len(widget.root_state) == 3
    with pytest.deprecated_call():
        assert len(state) == 5
    with pytest.deprecated_call():
        assert len(fill) == 1

    # Draw instructions show the new position
    assert widget._impl.draw_instructions == [
        "save",
        ("line to", {"x": 0, "y": 0}),
        "save",
        ("line to", {"x": 10, "y": 20}),
        # Begin fill
        "save",
        "begin path",
        ("line to", {"x": 25, "y": 25}),
        ("fill", {"fill_rule": FillRule.NONZERO}),
        "restore",
        # End fill
        ("line to", {"x": 30, "y": 40}),
        ("line to", {"x": 20, "y": 30}),
        ("line to", {"x": 40, "y": 50}),
        "restore",
        ("line to", {"x": 99, "y": 99}),
        "restore",
    ]

    with pytest.deprecated_call():
        # Remove the fill state
        state.remove(fill)

    # Counts are as expected
    with pytest.deprecated_call():
        assert len(widget.root_state) == 3
    with pytest.deprecated_call():
        assert len(state) == 4
    with pytest.deprecated_call():
        assert len(fill) == 1

    # Draw instructions show the new position
    assert widget._impl.draw_instructions == [
        "save",
        ("line to", {"x": 0, "y": 0}),
        "save",
        ("line to", {"x": 10, "y": 20}),
        ("line to", {"x": 30, "y": 40}),
        ("line to", {"x": 20, "y": 30}),
        ("line to", {"x": 40, "y": 50}),
        "restore",
        ("line to", {"x": 99, "y": 99}),
        "restore",
    ]

    with pytest.deprecated_call():
        # Insert the fill state at a negative index
        state.insert(-1, fill)

    # Draw instructions show the new position
    assert widget._impl.draw_instructions == [
        "save",
        ("line to", {"x": 0, "y": 0}),
        "save",
        ("line to", {"x": 10, "y": 20}),
        ("line to", {"x": 30, "y": 40}),
        ("line to", {"x": 20, "y": 30}),
        # Begin fill
        "save",
        "begin path",
        ("line to", {"x": 25, "y": 25}),
        ("fill", {"fill_rule": FillRule.NONZERO}),
        "restore",
        # End fill
        ("line to", {"x": 40, "y": 50}),
        "restore",
        ("line to", {"x": 99, "y": 99}),
        "restore",
    ]

    with pytest.deprecated_call():
        # Clear the state
        state.clear()

    # Counts are as expected
    with pytest.deprecated_call():
        assert len(widget.root_state) == 3
    with pytest.deprecated_call():
        assert len(state) == 0

    # No draw instructions other than the outer state.
    assert widget._impl.draw_instructions == [
        "save",
        ("line to", {"x": 0, "y": 0}),
        "save",
        "restore",
        ("line to", {"x": 99, "y": 99}),
        "restore",
    ]
