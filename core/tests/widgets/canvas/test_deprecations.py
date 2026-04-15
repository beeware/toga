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
    RoundRect,
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


def test_renamed_root_manager(widget):
    with pytest.deprecated_call():
        context_property = widget.context

    assert context_property is widget.root_manager


@pytest.mark.parametrize(
    "method_name, args, DrawingActionClass",
    [
        ("begin_path", (), BeginPath),
        ("close_path", (), ClosePath),
        ("ClosedPath", (), ClosePath),  # Deprecated alias
        ("ClosedPath", (0, 0), ClosePath),  # Deprecated alias with removed parameters
        ("move_to", (0, 0), MoveTo),
        ("line_to", (0, 0), LineTo),
        ("bezier_curve_to", (0, 0, 0, 0, 0, 0), BezierCurveTo),
        ("quadratic_curve_to", (0, 0, 0, 0), QuadraticCurveTo),
        ("arc", (0, 0, 0), Arc),
        ("ellipse", (0, 0, 0, 0), Ellipse),
        ("rect", (0, 0, 0, 0), Rect),
        ("round_rect", (0, 0, 0, 0, 0), RoundRect),
        ("fill", (), Fill),
        ("Fill", (), Fill),  # Deprecated alias
        ("Fill", (0, 0), Fill),  # Deprecated alias with removed parameters
        ("stroke", (), Stroke),
        ("Stroke", (), Stroke),  # Deprecated alias
        ("Stroke", (0, 0), Stroke),  # Deprecated alias with removed parameters
        ("write_text", ("",), WriteText),
        ("draw_image", None, DrawImage),
        ("rotate", (0,), Rotate),
        ("scale", (0, 0), Scale),
        ("translate", (0, 0), Translate),
        ("reset_transform", (), ResetTransform),
        ("state", (), State),
        ("Context", (), State),  # Deprecated alias
    ],
)
def test_manager_drawing_methods(app, widget, method_name, args, DrawingActionClass):
    """Context manager drawing methods are deprecated, but still work."""
    with widget.state() as manager:
        pass

    if DrawingActionClass is DrawImage:
        # Can't create image from path until app fixture is loaded.
        args = (toga.Image("resources/sample.png"),)

    # Add to a context manager that's neither active nor root, to make sure the actions
    # are going to the right place.
    with pytest.deprecated_call():
        drawing_action = getattr(manager, method_name)(*args)

    assert manager.drawing_actions == [drawing_action]
    assert isinstance(drawing_action, DrawingActionClass)
    assert_action_performed(widget, "redraw")


def test_canvas_context_method(widget):
    """canvas.Context is deprecated, and appends a context manager to the root context
    manager.
    """

    # Create a sub-manager to ensure the method appends to root, not the active
    # manager.
    with widget.state() as active_manager:
        pass

    with pytest.deprecated_call(
        match=r"The Context\(\) drawing method has been renamed to state\(\)"
    ):
        with widget.Context() as context:
            pass

    assert widget.root_manager.drawing_actions == [active_manager, context]


@pytest.mark.parametrize(
    "args, kwargs, xy_warning, has_move",
    [
        ((), {}, False, False),
        ((10, 20), {}, True, True),
        ((10,), {}, True, False),
        ((), {"x": 10, "y": 20}, True, True),
        ((), {"x": 10}, True, False),
        ((), {"y": 20}, True, False),
    ],
)
@pytest.mark.parametrize(
    "method_name, new_name",
    [
        ("ClosedPath", "close_path"),
        ("Fill", "fill"),
        ("Stroke", "stroke"),
    ],
)
def test_capitalized_canvas_methods_xy(
    widget, args, kwargs, xy_warning, has_move, method_name, new_name
):
    """Capitalized methods with (x, y) are deprecated, and append to root manager."""
    # Create a sub-manager to ensure the method appends to root, not the active manager.
    with widget.state() as active_manager:
        pass

    match = rf"The {method_name}\(\) drawing method has been renamed to {new_name}\(\)"
    if xy_warning:
        match += (
            r", and no longer accepts x and y coordinates as parameters\. Instead, "
            rf"call move_to\(x, y\) after entering the {new_name} context\."
        )

    with pytest.deprecated_call():
        with getattr(widget, method_name)(*args, **kwargs) as submanager:
            pass

    assert widget.root_manager.drawing_actions == [active_manager, submanager]
    if has_move:
        assert submanager.drawing_actions == [MoveTo(10, 20)]


def test_closed_path_with_xy_but_not_entered(widget):
    """ClosedPath(x, y), if never entered, moves but doesn't begin a new path."""
    with pytest.deprecated_call():
        widget.ClosedPath(10, 20)

    # The first and last instructions save/restore the root manager, and can be ignored.
    assert widget._impl.draw_instructions[1:-1] == [
        ("move to", {"x": 10, "y": 20}),
        "close path",
    ]


def test_manager_canvas_reference(widget):
    """Retrieving a widget's canvas is deprecated."""
    manager = widget.root_manager

    # Make another canvas, just to be sure we get the right one.
    _ = toga.Canvas()

    with pytest.deprecated_call():
        assert manager.canvas == widget


def test_manager_redraw(widget):
    """DrawingActionManager.redraw() is deprecated, but still works."""
    manager = widget.root_manager

    # Attach it to a second canvas.
    other = toga.Canvas()
    with pytest.deprecated_call():
        other.root_manager.append(manager)
    # Clear the redraw from the append
    EventLog.reset()

    # Check a canvas it's *not* attached to as well.
    unrelated = toga.Canvas()

    with pytest.deprecated_call():
        manager.redraw()

    assert_action_performed(widget, "redraw")
    assert_action_performed(other, "redraw")
    assert_action_not_performed(unrelated, "redraw")


def test_unattached_manager(widget):
    """An unattached manager doesn't have a canvas or redraw anything."""
    manager = State()

    with pytest.deprecated_call():
        assert manager.canvas is None

    with pytest.deprecated_call():
        manager.redraw()

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
    """The Canvas CamelCase methods are deprecated, and add to root manager."""
    with widget.state() as manager:
        # Test within an open sub-state, to verify it adds to root manager.
        with pytest.deprecated_call():
            drawing_action = getattr(widget, method_name)()

    assert widget.root_manager.drawing_actions == [manager, drawing_action]
    assert isinstance(drawing_action, DrawingActionClass)
    assert_action_performed(widget, "redraw")


def test_deprecated_list_methods(widget):
    """List-like manager methods still work, but are deprecated."""

    # Initially nothing on the manager.
    with pytest.deprecated_call():
        assert len(widget.root_manager) == 0

    # Set up an inner manager that has contained operations, including a sub-manager
    widget.line_to(0, 0)
    with widget.state() as manager:
        widget.line_to(10, 20)
        second = widget.line_to(20, 30)
        with widget.fill() as fill:
            widget.line_to(25, 25)
        widget.line_to(30, 40)
        widget.line_to(40, 50)
    widget.line_to(99, 99)

    # Counts are as expected
    with pytest.deprecated_call():
        assert len(widget.root_manager) == 3
    with pytest.deprecated_call():
        assert len(manager) == 5
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
        manager.remove(second)
    # Drawing actions are as expected
    with pytest.deprecated_call():
        assert len(widget.root_manager) == 3
    for i, cls in enumerate([LineTo, State, LineTo]):
        with pytest.deprecated_call():
            assert isinstance(widget.root_manager[i], cls)
    with pytest.deprecated_call():
        with pytest.raises(IndexError):
            widget.root_manager[3]

    with pytest.deprecated_call():
        assert len(manager) == 4
    with pytest.deprecated_call():
        assert len(fill) == 1

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
        manager.insert(3, second)

    # Counts are as expected
    with pytest.deprecated_call():
        assert len(widget.root_manager) == 3
    with pytest.deprecated_call():
        assert len(manager) == 5
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
        # Remove the fill manager
        manager.remove(fill)

    # Counts are as expected
    with pytest.deprecated_call():
        assert len(widget.root_manager) == 3
    with pytest.deprecated_call():
        assert len(manager) == 4
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
        # Insert the fill manager at a negative index
        manager.insert(-1, fill)

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
        # Clear the manager
        manager.clear()

    # Counts are as expected
    with pytest.deprecated_call():
        assert len(widget.root_manager) == 3
    with pytest.deprecated_call():
        assert len(manager) == 0

    # No draw instructions other than the outer manager.
    assert widget._impl.draw_instructions == [
        "save",
        ("line to", {"x": 0, "y": 0}),
        "save",
        "restore",
        ("line to", {"x": 99, "y": 99}),
        "restore",
    ]
