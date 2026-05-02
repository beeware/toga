from contextlib import contextmanager

import pytest

import toga
from toga import Canvas
from toga.colors import BLACK, CORNFLOWERBLUE, REBECCAPURPLE, Color
from toga.constants import FillRule
from toga.fonts import SYSTEM, SYSTEM_DEFAULT_FONT_SIZE, Font
from toga.widgets.canvas import ClosePath, Fill, State, Stroke
from toga.widgets.canvas.canvas import drawing_context_property
from toga_dummy.utils import assert_action_not_performed, assert_action_performed

BLACK_COLOR = Color.parse(BLACK)
CORNFLOWERBLUE_COLOR = Color.parse(CORNFLOWERBLUE)
REBECCAPURPLE_COLOR = Color.parse(REBECCAPURPLE)


def test_widget_created():
    """An empty canvas can be created."""
    widget = toga.Canvas()
    assert widget._impl.interface == widget
    assert_action_performed(widget, "create Canvas")

    assert widget.on_resize._raw is None
    assert widget.on_press._raw is None
    assert widget.on_activate._raw is None
    assert widget.on_release._raw is None
    assert widget.on_drag._raw is None
    assert widget.on_alt_press._raw is None
    assert widget.on_alt_release._raw is None
    assert widget.on_alt_drag._raw is None

    # Canvas has a root state
    assert isinstance(widget.root_state, State)


def test_create_with_value(
    widget,
    on_resize_handler,
    on_press_handler,
    on_activate_handler,
    on_release_handler,
    on_drag_handler,
    on_alt_press_handler,
    on_alt_release_handler,
    on_alt_drag_handler,
):
    """A Canvas can be created with initial values."""
    assert widget._impl.interface == widget
    assert_action_performed(widget, "create Canvas")

    assert widget.on_resize._raw == on_resize_handler
    assert widget.on_press._raw == on_press_handler
    assert widget.on_activate._raw == on_activate_handler
    assert widget.on_release._raw == on_release_handler
    assert widget.on_drag._raw == on_drag_handler
    assert widget.on_alt_press._raw == on_alt_press_handler
    assert widget.on_alt_release._raw == on_alt_release_handler
    assert widget.on_alt_drag._raw == on_alt_drag_handler

    # Canvas has a root state
    assert isinstance(widget.root_state, State)


def test_disable_no_op(widget):
    """Canvas doesn't have a disabled state."""
    # Enabled by default
    assert widget.enabled

    # Try to disable the widget
    widget.enabled = False

    # Still enabled.
    assert widget.enabled


def test_focus_noop(widget):
    """Focus is a no-op."""

    widget.focus()
    assert_action_not_performed(widget, "focus")


def test_redraw(widget):
    """The canvas can be redrawn."""
    widget.redraw()

    assert_action_performed(widget, "redraw")

    # An empty canvas has 2 draw operations - pushing and popping the root state.
    assert widget._impl.draw_instructions == [
        "save",
        "restore",
    ]


def test_closed_path(widget):
    """A canvas can produce a ClosedPath sub-state."""
    with widget.close_path() as closed_path:
        # A fresh state has been created as a sub-state of the canvas.
        assert isinstance(closed_path, ClosePath)
        assert closed_path is not widget.root_state


def test_fill(widget):
    """A canvas can produce a Fill sub-state."""
    with widget.fill(fill_rule=FillRule.EVENODD, fill_style=REBECCAPURPLE) as fill:
        # A fresh state has been created as a sub-state of the canvas.
        assert isinstance(fill, Fill)
        assert fill is not widget.root_state

        assert fill.fill_style == REBECCAPURPLE_COLOR
        assert fill.fill_rule == FillRule.EVENODD


def test_stroke(widget):
    """A canvas can produce a Stroke sub-state."""
    with widget.stroke(
        stroke_style=REBECCAPURPLE,
        line_width=5,
        line_dash=[2, 7],
    ) as stroke:
        # A fresh state has been created as a sub-state of the canvas.
        assert isinstance(stroke, Stroke)
        assert stroke is not widget.root_state

        assert stroke.stroke_style == REBECCAPURPLE_COLOR
        assert stroke.line_width == 5.0
        assert stroke.line_dash == [2, 7]


@pytest.mark.parametrize(
    "font, line_height, expected",
    [
        (None, None, (132, 12)),
        (Font(family=SYSTEM, size=SYSTEM_DEFAULT_FONT_SIZE), None, (132, 12)),
        (Font(family=SYSTEM, size=SYSTEM_DEFAULT_FONT_SIZE), 1, (132, 12)),
        (Font(family=SYSTEM, size=20), None, (220, 20)),
        (Font(family=SYSTEM, size=20), 1, (220, 20)),
        (Font(family=SYSTEM, size=20), 1.5, (220, 30)),
        (Font(family="Cutive", size=SYSTEM_DEFAULT_FONT_SIZE), None, (198, 18)),
        (Font(family="Cutive", size=SYSTEM_DEFAULT_FONT_SIZE), 1, (198, 18)),
        (Font(family="Cutive", size=20), None, (330, 30)),
        (Font(family="Cutive", size=20), 1, (330, 30)),
        (Font(family="Cutive", size=20), 1.5, (330, 45)),
    ],
)
def test_measure_text(widget, font, line_height, expected):
    """Canvas can measure rendered text size."""
    assert (
        widget.measure_text("Hello world", font=font, line_height=line_height)
        == expected
    )


@pytest.mark.parametrize(
    "font, line_height, expected",
    [
        (None, None, (132, 24)),
        (Font(family=SYSTEM, size=SYSTEM_DEFAULT_FONT_SIZE), None, (132, 24)),
        (Font(family=SYSTEM, size=SYSTEM_DEFAULT_FONT_SIZE), 1, (132, 24)),
        (Font(family=SYSTEM, size=20), None, (220, 40)),
        (Font(family=SYSTEM, size=20), 1, (220, 40)),
        (Font(family=SYSTEM, size=20), 1.5, (220, 60)),
        (Font(family="Cutive", size=SYSTEM_DEFAULT_FONT_SIZE), None, (198, 36)),
        (Font(family="Cutive", size=SYSTEM_DEFAULT_FONT_SIZE), 1, (198, 36)),
        (Font(family="Cutive", size=20), None, (330, 60)),
        (Font(family="Cutive", size=20), 1, (330, 60)),
        (Font(family="Cutive", size=20), 1.5, (330, 90)),
    ],
)
def test_measure_text_multiline(widget, font, line_height, expected):
    """Canvas can measure rendered text size of a multiline string."""
    assert (
        widget.measure_text("Hello\nworld", font=font, line_height=line_height)
        == expected
    )


def test_as_image(widget):
    """A rendered canvas can be retrieved as an image."""
    image = widget.as_image()
    assert image is not None
    assert_action_performed(widget, "get image data")


# Utility methods to abstract how context is saved and restored. Context attributes
# should behave the same whether one uses the state() context manager or the save() and
# restore() methods.


def state_context_manager(canvas):
    # Is already a context manager:
    return canvas.state()


@contextmanager
def save_and_restore(canvas):
    canvas.save()
    try:
        yield
    finally:
        canvas.restore()


@pytest.mark.parametrize(
    "name, default, assign_1, check_1, assign_2, check_2",
    [
        (
            "fill_style",
            BLACK_COLOR,
            REBECCAPURPLE,
            REBECCAPURPLE_COLOR,
            CORNFLOWERBLUE,
            CORNFLOWERBLUE_COLOR,
        ),
        (
            "stroke_style",
            BLACK_COLOR,
            REBECCAPURPLE,
            REBECCAPURPLE_COLOR,
            CORNFLOWERBLUE,
            CORNFLOWERBLUE_COLOR,
        ),
        ("line_width", 2.0, 5, 5.0, 10.0, 10.0),
        ("line_dash", [], [1, 2], [1.0, 2.0], [2.0, 3.0], [2.0, 3.0]),
    ],
)
@pytest.mark.parametrize("restore_method", [state_context_manager, save_and_restore])
def test_attributes_save_restore(
    widget, name, default, assign_1, check_1, assign_2, check_2, restore_method
):
    """Context attributes can be set, accessed, and restored, but not deleted."""
    assert getattr(widget, name) == default

    with restore_method(widget):
        assert getattr(widget, name) == default

        setattr(widget, name, assign_1)
        assert getattr(widget, name) == check_1

        with restore_method(widget):
            assert getattr(widget, name) == check_1
            setattr(widget, name, assign_2)
            assert getattr(widget, name) == check_2

        assert getattr(widget, name) == check_1

    assert getattr(widget, name) == default

    match = (
        r"Drawing context attributes can't be deleted or set to None\. To reset to a "
        r"default or previous value, do so explicitly or reset to a previous context "
        r"state\."
    )

    with pytest.raises(ValueError, match=match):
        delattr(widget, name)

    with pytest.raises(ValueError, match=match):
        setattr(widget, name, None)


@pytest.mark.parametrize(
    "attr_name",
    ["fill_style", "stroke_style", "line_width", "line_dash"],
)
def test_attribute_class_level_access(widget, attr_name):
    """Class-level access of a context attribute returns the property itself."""
    assert isinstance(getattr(Canvas, attr_name), drawing_context_property)
