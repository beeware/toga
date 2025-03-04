import pytest

import toga
from toga.colors import rgb
from toga.constants import FillRule
from toga.fonts import SYSTEM, SYSTEM_DEFAULT_FONT_SIZE, Font
from toga.widgets.canvas import ClosedPathContext, Context, FillContext, StrokeContext
from toga_dummy.utils import assert_action_not_performed, assert_action_performed

REBECCA_PURPLE_COLOR = rgb(102, 51, 153)


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

    # Canvas has a root context
    assert isinstance(widget.context, Context)


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

    # Canvas has a root context
    assert isinstance(widget.context, Context)


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

    # An empty canvas has 2 draw operations - pushing and popping the root context.
    assert widget._impl.draw_instructions == [
        ("push context", {}),
        ("pop context", {}),
    ]


def test_subcontext(widget):
    """A canvas can produce a subcontext."""
    with widget.Context() as subcontext:
        # A fresh context has been created as a subcontext of the canvas.
        assert isinstance(subcontext, Context)
        assert subcontext != widget.context


def test_closed_path(widget):
    """A canvas can produce a ClosedPath subcontext."""
    with widget.ClosedPath(x=10, y=20) as closed_path:
        # A fresh context has been created as a subcontext of the canvas.
        assert isinstance(closed_path, ClosedPathContext)
        assert closed_path != widget.context
        assert closed_path.x == 10
        assert closed_path.y == 20


def test_fill(widget):
    """A canvas can produce a Fill subcontext."""
    with widget.Fill(
        x=10, y=20, color="rebeccapurple", fill_rule=FillRule.EVENODD
    ) as fill:
        # A fresh context has been created as a subcontext of the canvas.
        assert isinstance(fill, FillContext)
        assert fill != widget.context

        assert fill.x == 10
        assert fill.y == 20
        assert fill.color == REBECCA_PURPLE_COLOR
        assert fill.fill_rule == FillRule.EVENODD


def test_stroke(widget):
    """A canvas can produce a Stroke subcontext."""
    with widget.Stroke(
        x=10, y=20, color="rebeccapurple", line_width=5, line_dash=[2, 7]
    ) as stroke:
        # A fresh context has been created as a subcontext of the canvas.
        assert isinstance(stroke, StrokeContext)
        assert stroke != widget.context

        assert stroke.x == 10
        assert stroke.y == 20
        assert stroke.color == REBECCA_PURPLE_COLOR
        assert stroke.line_width == 5.0
        assert stroke.line_dash == [2, 7]


@pytest.mark.parametrize(
    "font, line_height, expected",
    [
        (None, 1, (132, 12)),
        (Font(family=SYSTEM, size=SYSTEM_DEFAULT_FONT_SIZE), 1, (132, 12)),
        (Font(family=SYSTEM, size=20), 1, (220, 20)),
        (Font(family=SYSTEM, size=20), 1.5, (220, 30)),
        (Font(family="Cutive", size=SYSTEM_DEFAULT_FONT_SIZE), 1, (198, 18)),
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
        (None, 1, (132, 24)),
        (Font(family=SYSTEM, size=SYSTEM_DEFAULT_FONT_SIZE), 1, (132, 24)),
        (Font(family=SYSTEM, size=20), 1, (220, 40)),
        (Font(family=SYSTEM, size=20), 1.5, (220, 60)),
        (Font(family="Cutive", size=SYSTEM_DEFAULT_FONT_SIZE), 1, (198, 36)),
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
