import pytest

import toga
from toga.colors import rgb
from toga.constants import Baseline, FillRule
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
    "font, expected",
    [
        (None, (132, 12)),
        (Font(family=SYSTEM, size=SYSTEM_DEFAULT_FONT_SIZE), (132, 12)),
        (Font(family=SYSTEM, size=20), (220, 20)),
        (Font(family="Cutive", size=SYSTEM_DEFAULT_FONT_SIZE), (198, 18)),
        (Font(family="Cutive", size=20), (330, 30)),
    ],
)
def test_measure_text(widget, font, expected):
    """Canvas can measure rendered text size."""
    assert widget.measure_text("Hello world", font=font) == expected


def test_as_image(widget):
    """A rendered canvas can be retrieved as an image."""
    image = widget.as_image()
    assert image is not None
    assert_action_performed(widget, "get image data")


def test_deprecated_drawing_operations(widget):
    """Deprecated simple drawing operations raise a warning."""

    with pytest.warns(
        DeprecationWarning,
        match=r"Direct canvas operations have been deprecated; use context.begin_path()",
    ):
        widget.new_path()

    with pytest.warns(
        DeprecationWarning,
        match=r"Direct canvas operations have been deprecated; use context.move_to()",
    ):
        widget.move_to(10, 20)

    with pytest.warns(
        DeprecationWarning,
        match=r"Direct canvas operations have been deprecated; use context.line_to()",
    ):
        widget.line_to(10, 20)

    with pytest.warns(
        DeprecationWarning,
        match=r"Direct canvas operations have been deprecated; use context.bezier_curve_to()",
    ):
        widget.bezier_curve_to(1, 2, 3, 4, 10, 20)

    with pytest.warns(
        DeprecationWarning,
        match=r"Direct canvas operations have been deprecated; use context.quadratic_curve_to()",
    ):
        widget.quadratic_curve_to(1, 2, 10, 20)

    with pytest.warns(
        DeprecationWarning,
        match=r"Direct canvas operations have been deprecated; use context.arc()",
    ):
        widget.arc(10, 20, 30, 0.4, 0.5, True)

    with pytest.warns(
        DeprecationWarning,
        match=r"Direct canvas operations have been deprecated; use context.ellipse()",
    ):
        widget.ellipse(10, 20, 30, 40, 0.4, 0.5, 0.6, True)

    with pytest.warns(
        DeprecationWarning,
        match=r"Direct canvas operations have been deprecated; use context.rect()",
    ):
        widget.rect(10, 20, 30, 40)

    with pytest.warns(
        DeprecationWarning,
        match=r"Direct canvas operations have been deprecated; use context.write_text()",
    ):
        widget.write_text("Hello World", 10, 20, Font("Cutive", 37))

    with pytest.warns(
        DeprecationWarning,
        match=r"Direct canvas operations have been deprecated; use context.rotate()",
    ):
        widget.rotate(0.4)

    with pytest.warns(
        DeprecationWarning,
        match=r"Direct canvas operations have been deprecated; use context.scale()",
    ):
        widget.scale(0.4, 0.5)

    with pytest.warns(
        DeprecationWarning,
        match=r"Direct canvas operations have been deprecated; use context.translate()",
    ):
        widget.translate(10, 20)

    with pytest.warns(
        DeprecationWarning,
        match=r"Direct canvas operations have been deprecated; use context.reset_transform()",
    ):
        widget.reset_transform()

    with pytest.warns(
        DeprecationWarning,
        match=r"Canvas.closed_path\(\) has been renamed Canvas.ClosedPath\(\)",
    ):
        with widget.closed_path(10, 20) as closed_path:
            closed_path.line_to(20, 30)
            closed_path.line_to(30, 20)

    with pytest.warns(
        DeprecationWarning,
        match=r"Canvas.fill\(\) has been renamed Canvas.Fill\(\)",
    ):
        with widget.fill("rebeccapurple", FillRule.EVENODD) as fill:
            fill.line_to(20, 30)
            fill.line_to(30, 20)

    with pytest.warns(
        DeprecationWarning,
        match=r"Canvas.stroke\(\) has been renamed Canvas.Stroke\(\)",
    ):
        with widget.stroke("rebeccapurple", 3.0, [2, 7]) as stroke:
            stroke.line_to(20, 30)
            stroke.line_to(30, 20)

    # Assert the deprecated draw instructions rendered as expected
    assert widget._impl.draw_instructions == [
        ("push context", {}),
        ("begin path", {}),
        ("move to", {"x": 10, "y": 20}),
        ("line to", {"x": 10, "y": 20}),
        (
            "bezier curve to",
            {"cp1x": 1, "cp1y": 2, "cp2x": 3, "cp2y": 4, "x": 10, "y": 20},
        ),
        (
            "quadratic curve to",
            {"cpx": 1, "cpy": 2, "x": 10, "y": 20},
        ),
        (
            "arc",
            {
                "x": 10,
                "y": 20,
                "radius": 30,
                "startangle": 0.4,
                "endangle": 0.5,
                "anticlockwise": True,
            },
        ),
        (
            "ellipse",
            {
                "x": 10,
                "y": 20,
                "radiusx": 30,
                "radiusy": 40,
                "rotation": 0.4,
                "startangle": 0.5,
                "endangle": 0.6,
                "anticlockwise": True,
            },
        ),
        ("rect", {"x": 10, "y": 20, "width": 30, "height": 40}),
        (
            "write text",
            {
                "text": "Hello World",
                "x": 10,
                "y": 20,
                "font": Font("Cutive", 37)._impl,
                "baseline": Baseline.ALPHABETIC,
            },
        ),
        ("rotate", {"radians": 0.4}),
        ("scale", {"sx": 0.4, "sy": 0.5}),
        ("translate", {"tx": 10, "ty": 20}),
        ("reset transform", {}),
        # ClosedPath
        ("push context", {}),
        ("begin path", {}),
        ("move to", {"x": 10, "y": 20}),
        ("line to", {"x": 20, "y": 30}),
        ("line to", {"x": 30, "y": 20}),
        ("close path", {}),
        ("pop context", {}),
        # Fill
        ("push context", {}),
        ("begin path", {}),
        (
            "line to",
            {
                "x": 20,
                "y": 30,
                "fill_color": REBECCA_PURPLE_COLOR,
                "fill_rule": FillRule.EVENODD,
            },
        ),
        (
            "line to",
            {
                "x": 30,
                "y": 20,
                "fill_color": REBECCA_PURPLE_COLOR,
                "fill_rule": FillRule.EVENODD,
            },
        ),
        ("fill", {"color": REBECCA_PURPLE_COLOR, "fill_rule": FillRule.EVENODD}),
        ("pop context", {}),
        # Stroke
        ("push context", {}),
        ("begin path", {}),
        (
            "line to",
            {
                "x": 20,
                "y": 30,
                "stroke_color": REBECCA_PURPLE_COLOR,
                "line_width": 3.0,
                "line_dash": [2, 7],
            },
        ),
        (
            "line to",
            {
                "x": 30,
                "y": 20,
                "stroke_color": REBECCA_PURPLE_COLOR,
                "line_width": 3.0,
                "line_dash": [2, 7],
            },
        ),
        (
            "stroke",
            {"color": REBECCA_PURPLE_COLOR, "line_width": 3.0, "line_dash": [2, 7]},
        ),
        ("pop context", {}),
        ("pop context", {}),
    ]


def test_deprecated_args(widget):
    """Deprecated arguments to canvas functions raise warnings."""
    with pytest.warns(
        DeprecationWarning,
        match=r"The `tight` argument on Canvas.measure_text\(\) has been deprecated.",
    ):
        assert widget.measure_text(
            "Hello world", font=Font(family="Cutive", size=42), tight=True
        ) == (693, 63)

    with pytest.warns(
        DeprecationWarning,
        match=r"Canvas.fill\(\) has been renamed Canvas.Fill\(\)",
    ), pytest.warns(
        DeprecationWarning,
        match=r"The `preserve` argument on fill\(\) has been deprecated.",
    ):
        with widget.fill("rebeccapurple", FillRule.EVENODD, preserve=False) as fill:
            fill.line_to(20, 30)
            fill.line_to(30, 20)

    widget._impl.draw_instructions == [
        ("push context", {}),
        ("push context", {}),
        ("begin path", {}),
        ("line to", {"x": 20, "y": 30}),
        ("line to", {"x": 30, "y": 20}),
        ("fill", {"color": REBECCA_PURPLE_COLOR, "fill_rule": FillRule.EVENODD}),
        ("pop context", {}),
        ("pop context", {}),
    ]
