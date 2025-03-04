import pytest

from toga.colors import REBECCAPURPLE, rgb
from toga.constants import Baseline, FillRule
from toga.fonts import SYSTEM, SYSTEM_DEFAULT_FONT_SIZE, Font
from toga_dummy.utils import assert_action_performed

REBECCA_PURPLE_COLOR = rgb(102, 51, 153)


def test_begin_path(widget):
    """A begin path operation can be added."""
    draw_op = widget.context.begin_path()

    assert_action_performed(widget, "redraw")
    assert repr(draw_op) == "BeginPath()"

    # The first and last instructions can be ignored as they are the
    assert widget._impl.draw_instructions[1:-1] == [
        ("begin path", {}),
    ]


def test_close_path(widget):
    """A close path operation can be added."""
    draw_op = widget.context.close_path()

    assert_action_performed(widget, "redraw")
    assert repr(draw_op) == "ClosePath()"

    # The first and last instructions can be ignored as they are the
    assert widget._impl.draw_instructions[1:-1] == [
        ("close path", {}),
    ]


@pytest.mark.parametrize(
    "kwargs, args_repr, draw_kwargs",
    [
        # Defaults
        (
            {},
            "color=rgb(0, 0, 0), fill_rule=FillRule.NONZERO",
            {"color": rgb(0, 0, 0), "fill_rule": FillRule.NONZERO},
        ),
        # Color as string name
        (
            {"color": REBECCAPURPLE},
            f"color={REBECCA_PURPLE_COLOR}, fill_rule=FillRule.NONZERO",
            {"color": REBECCA_PURPLE_COLOR, "fill_rule": FillRule.NONZERO},
        ),
        # Color as RGB object
        (
            {"color": REBECCA_PURPLE_COLOR},
            f"color={REBECCA_PURPLE_COLOR}, fill_rule=FillRule.NONZERO",
            {"color": REBECCA_PURPLE_COLOR, "fill_rule": FillRule.NONZERO},
        ),
        # Color as RGB string
        (
            {"color": str(REBECCA_PURPLE_COLOR)},
            f"color={REBECCA_PURPLE_COLOR}, fill_rule=FillRule.NONZERO",
            {"color": REBECCA_PURPLE_COLOR, "fill_rule": FillRule.NONZERO},
        ),
        # Color reset with None
        (
            {"color": None},
            "color=rgb(0, 0, 0), fill_rule=FillRule.NONZERO",
            {"color": rgb(0, 0, 0), "fill_rule": FillRule.NONZERO},
        ),
        # Explicit Non-Zero winding
        (
            {"fill_rule": FillRule.NONZERO},
            "color=rgb(0, 0, 0), fill_rule=FillRule.NONZERO",
            {"color": rgb(0, 0, 0), "fill_rule": FillRule.NONZERO},
        ),
        # Even-Odd winding
        (
            {"fill_rule": FillRule.EVENODD},
            "color=rgb(0, 0, 0), fill_rule=FillRule.EVENODD",
            {"color": rgb(0, 0, 0), "fill_rule": FillRule.EVENODD},
        ),
        # All args
        (
            {"color": REBECCAPURPLE, "fill_rule": FillRule.EVENODD},
            f"color={REBECCA_PURPLE_COLOR}, fill_rule=FillRule.EVENODD",
            {"color": REBECCA_PURPLE_COLOR, "fill_rule": FillRule.EVENODD},
        ),
    ],
)
def test_fill(widget, kwargs, args_repr, draw_kwargs):
    """A primitive fill operation can be added."""
    draw_op = widget.context.fill(**kwargs)

    assert_action_performed(widget, "redraw")
    assert repr(draw_op) == f"Fill({args_repr})"

    # The first and last instructions can be ignored as they are the
    assert widget._impl.draw_instructions[1:-1] == [
        ("fill", draw_kwargs),
    ]

    # All the attributes can be retrieved.
    for attr, value in draw_kwargs.items():
        assert getattr(draw_op, attr) == value


@pytest.mark.parametrize(
    "kwargs, args_repr, draw_kwargs",
    [
        # Defaults
        (
            {},
            "color=rgb(0, 0, 0), line_width=2.0, line_dash=None",
            {"color": rgb(0, 0, 0), "line_width": 2.0, "line_dash": None},
        ),
        # Color as string name
        (
            {"color": REBECCAPURPLE},
            f"color={REBECCA_PURPLE_COLOR}, line_width=2.0, line_dash=None",
            {"color": REBECCA_PURPLE_COLOR, "line_width": 2.0, "line_dash": None},
        ),
        # Color as RGB object
        (
            {"color": REBECCA_PURPLE_COLOR},
            f"color={REBECCA_PURPLE_COLOR}, line_width=2.0, line_dash=None",
            {"color": REBECCA_PURPLE_COLOR, "line_width": 2.0, "line_dash": None},
        ),
        # Color as RGB string
        (
            {"color": str(REBECCA_PURPLE_COLOR)},
            f"color={REBECCA_PURPLE_COLOR}, line_width=2.0, line_dash=None",
            {"color": REBECCA_PURPLE_COLOR, "line_width": 2.0, "line_dash": None},
        ),
        # Color reset with None
        (
            {"color": None},
            "color=rgb(0, 0, 0), line_width=2.0, line_dash=None",
            {"color": rgb(0, 0, 0), "line_width": 2.0, "line_dash": None},
        ),
        # Line width
        (
            {"line_width": 4.5},
            "color=rgb(0, 0, 0), line_width=4.5, line_dash=None",
            {"color": rgb(0, 0, 0), "line_width": 4.5, "line_dash": None},
        ),
        # Line dash
        (
            {"line_dash": [2, 7]},
            "color=rgb(0, 0, 0), line_width=2.0, line_dash=[2, 7]",
            {"color": rgb(0, 0, 0), "line_width": 2.0, "line_dash": [2, 7]},
        ),
        # All args
        (
            {"color": REBECCAPURPLE, "line_width": 4.5, "line_dash": [2, 7]},
            f"color={REBECCA_PURPLE_COLOR}, line_width=4.5, line_dash=[2, 7]",
            {"color": REBECCA_PURPLE_COLOR, "line_width": 4.5, "line_dash": [2, 7]},
        ),
    ],
)
def test_stroke(widget, kwargs, args_repr, draw_kwargs):
    """A primitive stroke operation can be added."""
    draw_op = widget.context.stroke(**kwargs)

    assert_action_performed(widget, "redraw")
    assert repr(draw_op) == f"Stroke({args_repr})"

    # The first and last instructions can be ignored as they are the
    assert widget._impl.draw_instructions[1:-1] == [
        ("stroke", draw_kwargs),
    ]

    # All the attributes can be retrieved.
    for attr, value in draw_kwargs.items():
        assert getattr(draw_op, attr) == value


def test_move_to(widget):
    """A move to operation can be added."""
    draw_op = widget.context.move_to(10, 20)

    assert_action_performed(widget, "redraw")
    assert repr(draw_op) == "MoveTo(x=10, y=20)"

    # The first and last instructions can be ignored as they are the
    assert widget._impl.draw_instructions[1:-1] == [
        ("move to", {"x": 10, "y": 20}),
    ]

    # All the attributes can be retrieved.
    assert draw_op.x == 10
    assert draw_op.y == 20


def test_line_to(widget):
    """A line to operation can be added."""
    draw_op = widget.context.line_to(10, 20)

    assert_action_performed(widget, "redraw")
    assert repr(draw_op) == "LineTo(x=10, y=20)"

    # The first and last instructions can be ignored as they are the
    assert widget._impl.draw_instructions[1:-1] == [
        ("line to", {"x": 10, "y": 20}),
    ]

    # All the attributes can be retrieved.
    assert draw_op.x == 10
    assert draw_op.y == 20


def test_bezier_curve_to(widget):
    """A Bézier curve to operation can be added."""
    draw_op = widget.context.bezier_curve_to(10, 20, 30, 40, 50, 60)

    assert_action_performed(widget, "redraw")
    assert (
        repr(draw_op) == "BezierCurveTo(cp1x=10, cp1y=20, cp2x=30, cp2y=40, x=50, y=60)"
    )

    # The first and last instructions can be ignored as they are the
    assert widget._impl.draw_instructions[1:-1] == [
        (
            "bezier curve to",
            {"cp1x": 10, "cp1y": 20, "cp2x": 30, "cp2y": 40, "x": 50, "y": 60},
        ),
    ]

    # All the attributes can be retrieved.
    assert draw_op.cp1x == 10
    assert draw_op.cp1y == 20
    assert draw_op.cp2x == 30
    assert draw_op.cp2y == 40
    assert draw_op.x == 50
    assert draw_op.y == 60


def test_quadratic_curve_to(widget):
    """A Quadratic curve to operation can be added."""
    draw_op = widget.context.quadratic_curve_to(10, 20, 30, 40)

    assert_action_performed(widget, "redraw")
    assert repr(draw_op) == "QuadraticCurveTo(cpx=10, cpy=20, x=30, y=40)"

    # The first and last instructions can be ignored as they are the
    assert widget._impl.draw_instructions[1:-1] == [
        (
            "quadratic curve to",
            {"cpx": 10, "cpy": 20, "x": 30, "y": 40},
        ),
    ]

    # All the attributes can be retrieved.
    assert draw_op.cpx == 10
    assert draw_op.cpy == 20
    assert draw_op.x == 30
    assert draw_op.y == 40


@pytest.mark.parametrize(
    "kwargs, args_repr, draw_kwargs",
    [
        # Defaults
        (
            {"x": 10, "y": 20, "radius": 30},
            (
                "x=10, y=20, radius=30, startangle=0.000, "
                "endangle=6.283, anticlockwise=False"
            ),
            {
                "x": 10,
                "y": 20,
                "radius": 30,
                "startangle": 0.0,
                "endangle": pytest.approx(6.283185),
                "anticlockwise": False,
            },
        ),
        # Start angle
        (
            {"x": 10, "y": 20, "radius": 30, "startangle": 1.234},
            (
                "x=10, y=20, radius=30, startangle=1.234, "
                "endangle=6.283, anticlockwise=False"
            ),
            {
                "x": 10,
                "y": 20,
                "radius": 30,
                "startangle": pytest.approx(1.234),
                "endangle": pytest.approx(6.283185),
                "anticlockwise": False,
            },
        ),
        # End angle
        (
            {
                "x": 10,
                "y": 20,
                "radius": 30,
                "endangle": 2.345,
            },
            (
                "x=10, y=20, radius=30, startangle=0.000, "
                "endangle=2.345, anticlockwise=False"
            ),
            {
                "x": 10,
                "y": 20,
                "radius": 30,
                "startangle": 0.0,
                "endangle": pytest.approx(2.345),
                "anticlockwise": False,
            },
        ),
        # Anticlockwise explicitly False
        (
            {
                "x": 10,
                "y": 20,
                "radius": 30,
                "anticlockwise": False,
            },
            (
                "x=10, y=20, radius=30, startangle=0.000, "
                "endangle=6.283, anticlockwise=False"
            ),
            {
                "x": 10,
                "y": 20,
                "radius": 30,
                "startangle": 0.0,
                "endangle": pytest.approx(6.283185),
                "anticlockwise": False,
            },
        ),
        # Anticlockwise explicitly False
        (
            {
                "x": 10,
                "y": 20,
                "radius": 30,
                "anticlockwise": True,
            },
            (
                "x=10, y=20, radius=30, startangle=0.000, "
                "endangle=6.283, anticlockwise=True"
            ),
            {
                "x": 10,
                "y": 20,
                "radius": 30,
                "startangle": 0.0,
                "endangle": pytest.approx(6.283185),
                "anticlockwise": True,
            },
        ),
        # All args
        (
            {
                "x": 10,
                "y": 20,
                "radius": 30,
                "startangle": 1.234,
                "endangle": 2.345,
                "anticlockwise": True,
            },
            (
                "x=10, y=20, radius=30, startangle=1.234, "
                "endangle=2.345, anticlockwise=True"
            ),
            {
                "x": 10,
                "y": 20,
                "radius": 30,
                "startangle": pytest.approx(1.234),
                "endangle": pytest.approx(2.345),
                "anticlockwise": True,
            },
        ),
    ],
)
def test_arc(widget, kwargs, args_repr, draw_kwargs):
    """An arc operation can be added."""
    draw_op = widget.context.arc(**kwargs)

    assert_action_performed(widget, "redraw")
    assert repr(draw_op) == f"Arc({args_repr})"

    # The first and last instructions can be ignored as they are the
    assert widget._impl.draw_instructions[1:-1] == [
        ("arc", draw_kwargs),
    ]

    # All the attributes can be retrieved.
    for attr, value in draw_kwargs.items():
        assert getattr(draw_op, attr) == value


@pytest.mark.parametrize(
    "kwargs, args_repr, draw_kwargs",
    [
        # Defaults
        (
            {"x": 10, "y": 20, "radiusx": 30, "radiusy": 40},
            (
                "x=10, y=20, radiusx=30, radiusy=40, "
                "rotation=0.000, startangle=0.000, endangle=6.283, anticlockwise=False"
            ),
            {
                "x": 10,
                "y": 20,
                "radiusx": 30,
                "radiusy": 40,
                "rotation": 0.0,
                "startangle": 0.0,
                "endangle": pytest.approx(6.283185),
                "anticlockwise": False,
            },
        ),
        # Rotation
        (
            {"x": 10, "y": 20, "radiusx": 30, "radiusy": 40, "rotation": 1.234},
            (
                "x=10, y=20, radiusx=30, radiusy=40, "
                "rotation=1.234, startangle=0.000, endangle=6.283, anticlockwise=False"
            ),
            {
                "x": 10,
                "y": 20,
                "radiusx": 30,
                "radiusy": 40,
                "rotation": pytest.approx(1.234),
                "startangle": 0.0,
                "endangle": pytest.approx(6.283185),
                "anticlockwise": False,
            },
        ),
        # Start angle
        (
            {"x": 10, "y": 20, "radiusx": 30, "radiusy": 40, "startangle": 2.345},
            (
                "x=10, y=20, radiusx=30, radiusy=40, "
                "rotation=0.000, startangle=2.345, endangle=6.283, anticlockwise=False"
            ),
            {
                "x": 10,
                "y": 20,
                "radiusx": 30,
                "radiusy": 40,
                "rotation": 0.0,
                "startangle": pytest.approx(2.345),
                "endangle": pytest.approx(6.283185),
                "anticlockwise": False,
            },
        ),
        # End angle
        (
            {"x": 10, "y": 20, "radiusx": 30, "radiusy": 40, "endangle": 3.456},
            (
                "x=10, y=20, radiusx=30, radiusy=40, "
                "rotation=0.000, startangle=0.000, endangle=3.456, anticlockwise=False"
            ),
            {
                "x": 10,
                "y": 20,
                "radiusx": 30,
                "radiusy": 40,
                "rotation": 0.0,
                "startangle": 0.0,
                "endangle": pytest.approx(3.456),
                "anticlockwise": False,
            },
        ),
        # Anticlockwise explicitly False
        (
            {"x": 10, "y": 20, "radiusx": 30, "radiusy": 40, "anticlockwise": False},
            (
                "x=10, y=20, radiusx=30, radiusy=40, "
                "rotation=0.000, startangle=0.000, endangle=6.283, anticlockwise=False"
            ),
            {
                "x": 10,
                "y": 20,
                "radiusx": 30,
                "radiusy": 40,
                "rotation": 0.0,
                "startangle": 0.0,
                "endangle": pytest.approx(6.283185),
                "anticlockwise": False,
            },
        ),
        # Anticlockwise
        (
            {"x": 10, "y": 20, "radiusx": 30, "radiusy": 40, "anticlockwise": True},
            (
                "x=10, y=20, radiusx=30, radiusy=40, "
                "rotation=0.000, startangle=0.000, endangle=6.283, anticlockwise=True"
            ),
            {
                "x": 10,
                "y": 20,
                "radiusx": 30,
                "radiusy": 40,
                "rotation": 0.0,
                "startangle": 0.0,
                "endangle": pytest.approx(6.283185),
                "anticlockwise": True,
            },
        ),
        # All args
        (
            {
                "x": 10,
                "y": 20,
                "radiusx": 30,
                "radiusy": 40,
                "rotation": 1.234,
                "startangle": 2.345,
                "endangle": 3.456,
                "anticlockwise": True,
            },
            (
                "x=10, y=20, radiusx=30, radiusy=40, "
                "rotation=1.234, startangle=2.345, endangle=3.456, anticlockwise=True"
            ),
            {
                "x": 10,
                "y": 20,
                "radiusx": 30,
                "radiusy": 40,
                "rotation": pytest.approx(1.234),
                "startangle": pytest.approx(2.345),
                "endangle": pytest.approx(3.456),
                "anticlockwise": True,
            },
        ),
    ],
)
def test_ellipse(widget, kwargs, args_repr, draw_kwargs):
    """An ellipse operation can be added."""
    draw_op = widget.context.ellipse(**kwargs)

    assert_action_performed(widget, "redraw")
    assert repr(draw_op) == f"Ellipse({args_repr})"

    # The first and last instructions can be ignored as they are the
    assert widget._impl.draw_instructions[1:-1] == [
        ("ellipse", draw_kwargs),
    ]

    # All the attributes can be retrieved.
    for attr, value in draw_kwargs.items():
        assert getattr(draw_op, attr) == value


def test_rect(widget):
    """A rect operation can be added."""
    draw_op = widget.context.rect(10, 20, 30, 40)

    assert_action_performed(widget, "redraw")
    assert repr(draw_op) == "Rect(x=10, y=20, width=30, height=40)"

    # The first and last instructions can be ignored as they are the
    assert widget._impl.draw_instructions[1:-1] == [
        ("rect", {"x": 10, "y": 20, "width": 30, "height": 40}),
    ]

    # All the attributes can be retrieved.
    assert draw_op.x == 10
    assert draw_op.y == 20
    assert draw_op.width == 30
    assert draw_op.height == 40


@pytest.mark.parametrize(
    "kwargs, args_repr, draw_kwargs",
    [
        # Defaults
        (
            {"text": "Hello world", "x": 10, "y": 20},
            "text='Hello world', x=10, y=20, font=<Font: system default size system>, "
            "baseline=Baseline.ALPHABETIC, line_height=1",
            {
                "text": "Hello world",
                "x": 10,
                "y": 20,
                "font": Font(SYSTEM, SYSTEM_DEFAULT_FONT_SIZE)._impl,
                "baseline": Baseline.ALPHABETIC,
                "line_height": 1,
            },
        ),
        # Baseline
        (
            {"text": "Hello world", "x": 10, "y": 20, "baseline": Baseline.TOP},
            "text='Hello world', x=10, y=20, font=<Font: system default size system>, "
            "baseline=Baseline.TOP, line_height=1",
            {
                "text": "Hello world",
                "x": 10,
                "y": 20,
                "font": Font(SYSTEM, SYSTEM_DEFAULT_FONT_SIZE)._impl,
                "baseline": Baseline.TOP,
                "line_height": 1,
            },
        ),
        # Font
        (
            {"text": "Hello world", "x": 10, "y": 20, "font": Font("Cutive", 42)},
            "text='Hello world', x=10, y=20, font=<Font: 42pt Cutive>, "
            "baseline=Baseline.ALPHABETIC, line_height=1",
            {
                "text": "Hello world",
                "x": 10,
                "y": 20,
                "font": Font("Cutive", 42)._impl,
                "baseline": Baseline.ALPHABETIC,
                "line_height": 1,
            },
        ),
        # Line height factor
        (
            {"text": "Hello world", "x": 10, "y": 20, "line_height": 1.5},
            "text='Hello world', x=10, y=20, font=<Font: system default size system>, "
            "baseline=Baseline.ALPHABETIC, line_height=1.5",
            {
                "text": "Hello world",
                "x": 10,
                "y": 20,
                "font": Font(SYSTEM, SYSTEM_DEFAULT_FONT_SIZE)._impl,
                "baseline": Baseline.ALPHABETIC,
                "line_height": 1.5,
            },
        ),
    ],
)
def test_write_text(widget, kwargs, args_repr, draw_kwargs):
    """A write text operation can be added."""
    draw_op = widget.context.write_text(**kwargs)

    assert_action_performed(widget, "redraw")
    assert repr(draw_op) == f"WriteText({args_repr})"

    # The first and last instructions can be ignored as they are the
    assert widget._impl.draw_instructions[1:-1] == [
        ("write text", draw_kwargs),
    ]

    # All the attributes can be retrieved.
    assert draw_op.text == draw_kwargs["text"]
    assert draw_op.x == draw_kwargs["x"]
    assert draw_op.y == draw_kwargs["y"]
    assert draw_op.font == draw_kwargs["font"].interface
    assert draw_op.baseline == draw_kwargs["baseline"]
    assert draw_op.line_height == draw_kwargs["line_height"]


def test_rotate(widget):
    """A rotate operation can be added."""
    draw_op = widget.context.rotate(1.234)

    assert_action_performed(widget, "redraw")
    assert repr(draw_op) == "Rotate(radians=1.234)"

    # The first and last instructions can be ignored as they are the
    assert widget._impl.draw_instructions[1:-1] == [
        ("rotate", {"radians": pytest.approx(1.234)}),
    ]

    # All the attributes can be retrieved.
    assert draw_op.radians == pytest.approx(1.234)


def test_scale(widget):
    """A scale operation can be added."""
    draw_op = widget.context.scale(1.234, 2.345)

    assert_action_performed(widget, "redraw")
    assert repr(draw_op) == "Scale(sx=1.234, sy=2.345)"

    # The first and last instructions can be ignored as they are the
    assert widget._impl.draw_instructions[1:-1] == [
        ("scale", {"sx": pytest.approx(1.234), "sy": pytest.approx(2.345)}),
    ]

    # All the attributes can be retrieved.
    assert draw_op.sx == pytest.approx(1.234)
    assert draw_op.sy == pytest.approx(2.345)


def test_translate(widget):
    """A translate operation can be added."""
    draw_op = widget.context.translate(10, 20)

    assert_action_performed(widget, "redraw")
    assert repr(draw_op) == "Translate(tx=10, ty=20)"

    # The first and last instructions can be ignored as they are the
    assert widget._impl.draw_instructions[1:-1] == [
        ("translate", {"tx": 10, "ty": 20}),
    ]

    # All the attributes can be retrieved.
    assert draw_op.tx == 10
    assert draw_op.ty == 20


def test_reset_transform(widget):
    """A reset transform operation can be added."""
    draw_op = widget.context.reset_transform()

    assert_action_performed(widget, "redraw")
    assert repr(draw_op) == "ResetTransform()"

    # The first and last instructions can be ignored as they are the
    assert widget._impl.draw_instructions[1:-1] == [
        ("reset transform", {}),
    ]
