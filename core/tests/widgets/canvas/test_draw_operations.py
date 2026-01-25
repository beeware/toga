from pathlib import Path

import pytest

from toga.colors import REBECCAPURPLE, rgb
from toga.constants import Baseline, FillRule
from toga.fonts import SYSTEM, SYSTEM_DEFAULT_FONT_SIZE, Font
from toga.images import Image
from toga.widgets.canvas import Arc, Ellipse
from toga_dummy.utils import assert_action_performed

REBECCA_PURPLE_COLOR = rgb(102, 51, 153)
ABSOLUTE_FILE_PATH = Path(__file__).parent.parent.parent / "resources/toga.png"


def test_begin_path(widget):
    """A begin path operation can be added."""
    draw_op = widget.context.begin_path()

    assert_action_performed(widget, "redraw")
    assert repr(draw_op) == "BeginPath()"

    # The first and last instructions push/pull the root context, and can be ignored.
    assert widget._impl.draw_instructions[1:-1] == ["begin path"]


def test_close_path(widget):
    """A close path operation can be added."""
    draw_op = widget.context.close_path()

    assert_action_performed(widget, "redraw")
    assert repr(draw_op) == "ClosePath()"

    # The first and last instructions push/pull the root context, and can be ignored.
    assert widget._impl.draw_instructions[1:-1] == ["close path"]


@pytest.mark.parametrize(
    "kwargs, args_repr, draw_objs, attrs",
    [
        # Defaults
        (
            {},
            "color=None, fill_rule=FillRule.NONZERO",
            [("fill", {"fill_rule": FillRule.NONZERO})],
            {"color": None, "fill_rule": FillRule.NONZERO},
        ),
        # Color as string name
        (
            {"color": REBECCAPURPLE},
            f"color={REBECCA_PURPLE_COLOR!r}, fill_rule=FillRule.NONZERO",
            [
                ("set fill style", REBECCA_PURPLE_COLOR),
                ("fill", {"fill_rule": FillRule.NONZERO}),
            ],
            {"color": REBECCA_PURPLE_COLOR, "fill_rule": FillRule.NONZERO},
        ),
        # Color as RGB object
        (
            {"color": REBECCA_PURPLE_COLOR},
            f"color={REBECCA_PURPLE_COLOR!r}, fill_rule=FillRule.NONZERO",
            [
                ("set fill style", REBECCA_PURPLE_COLOR),
                ("fill", {"fill_rule": FillRule.NONZERO}),
            ],
            {"color": REBECCA_PURPLE_COLOR, "fill_rule": FillRule.NONZERO},
        ),
        # Color explicitly not set
        (
            {"color": None},
            "color=None, fill_rule=FillRule.NONZERO",
            [("fill", {"fill_rule": FillRule.NONZERO})],
            {"color": None, "fill_rule": FillRule.NONZERO},
        ),
        # Explicit Non-Zero winding
        (
            {"fill_rule": FillRule.NONZERO},
            "color=None, fill_rule=FillRule.NONZERO",
            [("fill", {"fill_rule": FillRule.NONZERO})],
            {"color": None, "fill_rule": FillRule.NONZERO},
        ),
        # Even-Odd winding
        (
            {"fill_rule": FillRule.EVENODD},
            "color=None, fill_rule=FillRule.EVENODD",
            [("fill", {"fill_rule": FillRule.EVENODD})],
            {"color": None, "fill_rule": FillRule.EVENODD},
        ),
        # All args
        (
            {"color": REBECCAPURPLE, "fill_rule": FillRule.EVENODD},
            f"color={REBECCA_PURPLE_COLOR!r}, fill_rule=FillRule.EVENODD",
            [
                ("set fill style", REBECCA_PURPLE_COLOR),
                ("fill", {"fill_rule": FillRule.EVENODD}),
            ],
            {"color": REBECCA_PURPLE_COLOR, "fill_rule": FillRule.EVENODD},
        ),
    ],
)
def test_fill(widget, kwargs, args_repr, draw_objs, attrs):
    """A primitive fill operation can be added."""
    draw_op = widget.context.fill(**kwargs)

    assert_action_performed(widget, "redraw")
    assert repr(draw_op) == f"Fill({args_repr})"

    # The first and last instructions push/pull the root context, and can be ignored.
    # But the fill itself also saves and then restores.
    assert widget._impl.draw_instructions[1:-1] == ["save", *draw_objs, "restore"]

    # All the attributes can be retrieved.
    for name, value in attrs.items():
        assert getattr(draw_op, name) == value


@pytest.mark.parametrize(
    "kwargs, args_repr, draw_objs, attrs",
    [
        # Defaults
        (
            {},
            "color=None, line_width=None, line_dash=None",
            [],
            {"color": None, "line_width": None, "line_dash": None},
        ),
        # Color as string name
        (
            {"color": REBECCAPURPLE},
            f"color={REBECCA_PURPLE_COLOR!r}, line_width=None, line_dash=None",
            [("set stroke style", REBECCA_PURPLE_COLOR)],
            {"color": REBECCA_PURPLE_COLOR, "line_width": None, "line_dash": None},
        ),
        # Color as RGB object
        (
            {"color": REBECCA_PURPLE_COLOR},
            f"color={REBECCA_PURPLE_COLOR!r}, line_width=None, line_dash=None",
            [("set stroke style", REBECCA_PURPLE_COLOR)],
            {"color": REBECCA_PURPLE_COLOR, "line_width": None, "line_dash": None},
        ),
        # Color explicitly not set
        (
            {"color": None},
            "color=None, line_width=None, line_dash=None",
            [],
            {"color": None, "line_width": None, "line_dash": None},
        ),
        # Line width
        (
            {"line_width": 4.5},
            "color=None, line_width=4.500, line_dash=None",
            [("set line width", 4.5)],
            {"color": None, "line_width": 4.5, "line_dash": None},
        ),
        # Line dash
        (
            {"line_dash": [2, 7]},
            "color=None, line_width=None, line_dash=[2, 7]",
            [("set line dash", [2, 7])],
            {"color": None, "line_width": None, "line_dash": [2, 7]},
        ),
        # All args
        (
            {"color": REBECCAPURPLE, "line_width": 4.5, "line_dash": [2, 7]},
            f"color={REBECCA_PURPLE_COLOR!r}, line_width=4.500, line_dash=[2, 7]",
            [
                ("set stroke style", REBECCA_PURPLE_COLOR),
                ("set line width", 4.5),
                ("set line dash", [2, 7]),
            ],
            {"color": REBECCA_PURPLE_COLOR, "line_width": 4.5, "line_dash": [2, 7]},
        ),
    ],
)
def test_stroke(widget, kwargs, args_repr, draw_objs, attrs):
    """A primitive stroke operation can be added."""
    draw_op = widget.context.stroke(**kwargs)

    assert_action_performed(widget, "redraw")
    assert repr(draw_op) == f"Stroke({args_repr})"

    # The first and last instructions push/pull the root context, and can be ignored.
    # But the stroke itself also saves and then restores.
    assert widget._impl.draw_instructions[1:-1] == [
        "save",
        *draw_objs,
        "stroke",
        "restore",
    ]

    # All the attributes can be retrieved.
    for name, value in attrs.items():
        assert getattr(draw_op, name) == value


def test_move_to(widget):
    """A move to operation can be added."""
    draw_op = widget.context.move_to(10, 20)

    assert_action_performed(widget, "redraw")
    assert repr(draw_op) == "MoveTo(x=10, y=20)"

    # The first and last instructions push/pull the root context, and can be ignored.
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

    # The first and last instructions push/pull the root context, and can be ignored.
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

    # The first and last instructions push/pull the root context, and can be ignored.
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

    # The first and last instructions push/pull the root context, and can be ignored.
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
                "endangle=6.283, counterclockwise=False"
            ),
            {
                "x": 10,
                "y": 20,
                "radius": 30,
                "startangle": 0.0,
                "endangle": pytest.approx(6.283185),
                "counterclockwise": False,
            },
        ),
        # Start angle
        (
            {"x": 10, "y": 20, "radius": 30, "startangle": 1.234},
            (
                "x=10, y=20, radius=30, startangle=1.234, "
                "endangle=6.283, counterclockwise=False"
            ),
            {
                "x": 10,
                "y": 20,
                "radius": 30,
                "startangle": pytest.approx(1.234),
                "endangle": pytest.approx(6.283185),
                "counterclockwise": False,
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
                "endangle=2.345, counterclockwise=False"
            ),
            {
                "x": 10,
                "y": 20,
                "radius": 30,
                "startangle": 0.0,
                "endangle": pytest.approx(2.345),
                "counterclockwise": False,
            },
        ),
        # Counterclockwise explicitly False
        (
            {
                "x": 10,
                "y": 20,
                "radius": 30,
                "counterclockwise": False,
            },
            (
                "x=10, y=20, radius=30, startangle=0.000, "
                "endangle=6.283, counterclockwise=False"
            ),
            {
                "x": 10,
                "y": 20,
                "radius": 30,
                "startangle": 0.0,
                "endangle": pytest.approx(6.283185),
                "counterclockwise": False,
            },
        ),
        # Counterclockwise explicitly False
        (
            {
                "x": 10,
                "y": 20,
                "radius": 30,
                "counterclockwise": True,
            },
            (
                "x=10, y=20, radius=30, startangle=0.000, "
                "endangle=6.283, counterclockwise=True"
            ),
            {
                "x": 10,
                "y": 20,
                "radius": 30,
                "startangle": 0.0,
                "endangle": pytest.approx(6.283185),
                "counterclockwise": True,
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
                "counterclockwise": True,
            },
            (
                "x=10, y=20, radius=30, startangle=1.234, "
                "endangle=2.345, counterclockwise=True"
            ),
            {
                "x": 10,
                "y": 20,
                "radius": 30,
                "startangle": pytest.approx(1.234),
                "endangle": pytest.approx(2.345),
                "counterclockwise": True,
            },
        ),
    ],
)
def test_arc(widget, kwargs, args_repr, draw_kwargs):
    """An arc operation can be added."""
    draw_op = widget.context.arc(**kwargs)

    assert_action_performed(widget, "redraw")
    assert repr(draw_op) == f"Arc({args_repr})"

    # The first and last instructions push/pull the root context, and can be ignored.
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
                "rotation=0.000, startangle=0.000, endangle=6.283, "
                "counterclockwise=False"
            ),
            {
                "x": 10,
                "y": 20,
                "radiusx": 30,
                "radiusy": 40,
                "rotation": 0.0,
                "startangle": 0.0,
                "endangle": pytest.approx(6.283185),
                "counterclockwise": False,
            },
        ),
        # Rotation
        (
            {"x": 10, "y": 20, "radiusx": 30, "radiusy": 40, "rotation": 1.234},
            (
                "x=10, y=20, radiusx=30, radiusy=40, "
                "rotation=1.234, startangle=0.000, endangle=6.283, "
                "counterclockwise=False"
            ),
            {
                "x": 10,
                "y": 20,
                "radiusx": 30,
                "radiusy": 40,
                "rotation": pytest.approx(1.234),
                "startangle": 0.0,
                "endangle": pytest.approx(6.283185),
                "counterclockwise": False,
            },
        ),
        # Start angle
        (
            {"x": 10, "y": 20, "radiusx": 30, "radiusy": 40, "startangle": 2.345},
            (
                "x=10, y=20, radiusx=30, radiusy=40, "
                "rotation=0.000, startangle=2.345, endangle=6.283, "
                "counterclockwise=False"
            ),
            {
                "x": 10,
                "y": 20,
                "radiusx": 30,
                "radiusy": 40,
                "rotation": 0.0,
                "startangle": pytest.approx(2.345),
                "endangle": pytest.approx(6.283185),
                "counterclockwise": False,
            },
        ),
        # End angle
        (
            {"x": 10, "y": 20, "radiusx": 30, "radiusy": 40, "endangle": 3.456},
            (
                "x=10, y=20, radiusx=30, radiusy=40, "
                "rotation=0.000, startangle=0.000, endangle=3.456, "
                "counterclockwise=False"
            ),
            {
                "x": 10,
                "y": 20,
                "radiusx": 30,
                "radiusy": 40,
                "rotation": 0.0,
                "startangle": 0.0,
                "endangle": pytest.approx(3.456),
                "counterclockwise": False,
            },
        ),
        # Counterclockwise explicitly False
        (
            {"x": 10, "y": 20, "radiusx": 30, "radiusy": 40, "counterclockwise": False},
            (
                "x=10, y=20, radiusx=30, radiusy=40, "
                "rotation=0.000, startangle=0.000, endangle=6.283, "
                "counterclockwise=False"
            ),
            {
                "x": 10,
                "y": 20,
                "radiusx": 30,
                "radiusy": 40,
                "rotation": 0.0,
                "startangle": 0.0,
                "endangle": pytest.approx(6.283185),
                "counterclockwise": False,
            },
        ),
        # Counterclockwise
        (
            {"x": 10, "y": 20, "radiusx": 30, "radiusy": 40, "counterclockwise": True},
            (
                "x=10, y=20, radiusx=30, radiusy=40, "
                "rotation=0.000, startangle=0.000, endangle=6.283, "
                "counterclockwise=True"
            ),
            {
                "x": 10,
                "y": 20,
                "radiusx": 30,
                "radiusy": 40,
                "rotation": 0.0,
                "startangle": 0.0,
                "endangle": pytest.approx(6.283185),
                "counterclockwise": True,
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
                "counterclockwise": True,
            },
            (
                "x=10, y=20, radiusx=30, radiusy=40, "
                "rotation=1.234, startangle=2.345, endangle=3.456, "
                "counterclockwise=True"
            ),
            {
                "x": 10,
                "y": 20,
                "radiusx": 30,
                "radiusy": 40,
                "rotation": pytest.approx(1.234),
                "startangle": pytest.approx(2.345),
                "endangle": pytest.approx(3.456),
                "counterclockwise": True,
            },
        ),
    ],
)
def test_ellipse(widget, kwargs, args_repr, draw_kwargs):
    """An ellipse operation can be added."""
    draw_op = widget.context.ellipse(**kwargs)

    assert_action_performed(widget, "redraw")
    assert repr(draw_op) == f"Ellipse({args_repr})"

    # The first and last instructions push/pull the root context, and can be ignored.
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

    # The first and last instructions push/pull the root context, and can be ignored.
    assert widget._impl.draw_instructions[1:-1] == [
        ("rect", {"x": 10, "y": 20, "width": 30, "height": 40}),
    ]

    # All the attributes can be retrieved.
    assert draw_op.x == 10
    assert draw_op.y == 20
    assert draw_op.width == 30
    assert draw_op.height == 40


SYSTEM_FONT_IMPL = Font(SYSTEM, SYSTEM_DEFAULT_FONT_SIZE)._impl


@pytest.mark.parametrize(
    "kwargs, instructions, args_repr, draw_attrs",
    [
        # Defaults
        (
            {"text": "Hello world", "x": 10, "y": 20},
            # When font isn't specified, the system font is still supplied to the
            # backend.
            {
                "text": "Hello world",
                "x": 10,
                "y": 20,
                "baseline": Baseline.ALPHABETIC,
                "line_height": None,
                "font": SYSTEM_FONT_IMPL,
            },
            (
                "text='Hello world', x=10, y=20, font=None, "
                "baseline=Baseline.ALPHABETIC, line_height=None"
            ),
            {
                "text": "Hello world",
                "x": 10,
                "y": 20,
                "font": None,
                "baseline": Baseline.ALPHABETIC,
                "line_height": None,
            },
        ),
        # Baseline
        (
            {"text": "Hello world", "x": 10, "y": 20, "baseline": Baseline.TOP},
            {
                "text": "Hello world",
                "x": 10,
                "y": 20,
                "baseline": Baseline.TOP,
                "line_height": None,
                "font": SYSTEM_FONT_IMPL,
            },
            (
                "text='Hello world', x=10, y=20, font=None, "
                "baseline=Baseline.TOP, line_height=None"
            ),
            {
                "text": "Hello world",
                "x": 10,
                "y": 20,
                "font": None,
                "baseline": Baseline.TOP,
                "line_height": None,
            },
        ),
        # Font
        (
            {"text": "Hello world", "x": 10, "y": 20, "font": Font("Cutive", 42)},
            {
                "text": "Hello world",
                "x": 10,
                "y": 20,
                "baseline": Baseline.ALPHABETIC,
                "line_height": None,
                "font": Font("Cutive", 42)._impl,
            },
            (
                "text='Hello world', x=10, y=20, font=<Font: 42pt Cutive>, "
                "baseline=Baseline.ALPHABETIC, line_height=None"
            ),
            {
                "text": "Hello world",
                "x": 10,
                "y": 20,
                "font": Font("Cutive", 42),
                "baseline": Baseline.ALPHABETIC,
                "line_height": None,
            },
        ),
        # Line height factor
        (
            {"text": "Hello world", "x": 10, "y": 20, "line_height": 1.5},
            {
                "text": "Hello world",
                "x": 10,
                "y": 20,
                "baseline": Baseline.ALPHABETIC,
                "line_height": 1.5,
                "font": SYSTEM_FONT_IMPL,
            },
            (
                "text='Hello world', x=10, y=20, font=None, "
                "baseline=Baseline.ALPHABETIC, line_height=1.500"
            ),
            {
                "text": "Hello world",
                "x": 10,
                "y": 20,
                "font": None,
                "baseline": Baseline.ALPHABETIC,
                "line_height": 1.5,
            },
        ),
    ],
)
def test_write_text(widget, kwargs, instructions, args_repr, draw_attrs):
    """A write text operation can be added."""
    draw_op = widget.context.write_text(**kwargs)

    assert_action_performed(widget, "redraw")
    assert repr(draw_op) == f"WriteText({args_repr})"

    # The first and last instructions push/pull the root context, and can be ignored.
    assert widget._impl.draw_instructions[1:-1] == [
        ("write text", instructions),
    ]

    # All the attributes can be retrieved.
    assert draw_op.text == draw_attrs["text"]
    assert draw_op.x == draw_attrs["x"]
    assert draw_op.y == draw_attrs["y"]
    assert draw_op.font == draw_attrs["font"]
    assert draw_op.baseline == draw_attrs["baseline"]
    assert draw_op.line_height == draw_attrs["line_height"]


def test_rotate(widget):
    """A rotate operation can be added."""
    draw_op = widget.context.rotate(1.234)

    assert_action_performed(widget, "redraw")
    assert repr(draw_op) == "Rotate(radians=1.234)"

    # The first and last instructions push/pull the root context, and can be ignored.
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

    # The first and last instructions push/pull the root context, and can be ignored.
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

    # The first and last instructions push/pull the root context, and can be ignored.
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

    # The first and last instructions push/pull the root context, and can be ignored.
    assert widget._impl.draw_instructions[1:-1] == ["reset transform"]


@pytest.mark.parametrize(
    "kwargs, instructions, args_repr, draw_attrs",
    [
        # Defaults
        (
            {"x": 10, "y": 20},
            # When width and height aren't specified, the image's true dimensions are
            # supplied to the backend.
            {"x": 10, "y": 20, "width": 32, "height": 32},
            "x=10, y=20, width=None, height=None",
            {
                "x": 10,
                "y": 20,
                "width": None,
                "height": None,
            },
        ),
        # Into rectangle
        (
            {
                "x": 10,
                "y": 20,
                "width": 100,
                "height": 50,
            },
            {
                "x": 10,
                "y": 20,
                "width": 100,
                "height": 50,
            },
            "x=10, y=20, width=100, height=50",
            {
                "x": 10,
                "y": 20,
                "width": 100,
                "height": 50,
            },
        ),
    ],
)
def test_draw_image(app, widget, kwargs, instructions, args_repr, draw_attrs):
    """An image can be drawn."""
    image = Image(ABSOLUTE_FILE_PATH)
    draw_op = widget.context.draw_image(image=image, **kwargs)

    assert_action_performed(widget, "redraw")
    assert repr(draw_op) == f"DrawImage(image={image!r}, {args_repr})"

    # The first and last instructions push/pull the root context, and can be ignored.
    instructions["image"] = image
    assert widget._impl.draw_instructions[1:-1] == [
        ("draw_image", instructions),
    ]

    # All the attributes can be retrieved.
    assert draw_op.image == image
    assert draw_op.x == draw_attrs["x"]
    assert draw_op.y == draw_attrs["y"]
    assert draw_op.width == draw_attrs["width"]
    assert draw_op.height == draw_attrs["height"]


@pytest.mark.parametrize("value", [True, False])
def test_anticlockwise_deprecated(widget, value):
    """The 'anticlockwise' parameter is deprecated."""
    match = (
        r"Parameter 'anticlockwise' is deprecated\. Use 'counterclockwise' instead\."
    )

    with pytest.warns(DeprecationWarning, match=match):
        widget.context.arc(x=0, y=0, radius=10, anticlockwise=value)

    with pytest.warns(DeprecationWarning, match=match):
        Arc(x=0, y=0, radius=10, anticlockwise=value)

    with pytest.warns(DeprecationWarning, match=match):
        widget.context.ellipse(x=0, y=0, radiusx=10, radiusy=10, anticlockwise=value)

    with pytest.warns(DeprecationWarning, match=match):
        Ellipse(x=0, y=0, radiusx=10, radiusy=10, anticlockwise=value)


@pytest.mark.parametrize("anti", [True, False])
@pytest.mark.parametrize("counter", [True, False])
def test_anticlockwise_invalid(widget, anti, counter):
    """Providing both 'anticlockwise' and 'counterclockwise' raises a TypeError.

    Theoretically we should be able to proceed with the drawing operation (and only
    issue a deprecation warning) if the two values supplied agree, but truthy/falsey
    values could cause confusing errors.
    """
    match = r"Received both 'anticlockwise' and 'counterclockwise' arguments"

    with pytest.raises(TypeError, match=match):
        widget.context.arc(
            x=0, y=0, radius=10, anticlockwise=anti, counterclockwise=counter
        )

    with pytest.raises(TypeError, match=match):
        Arc(x=0, y=0, radius=10, anticlockwise=anti, counterclockwise=counter)

    with pytest.raises(TypeError, match=match):
        widget.context.ellipse(
            x=0,
            y=0,
            radiusx=10,
            radiusy=10,
            anticlockwise=anti,
            counterclockwise=counter,
        )

    with pytest.raises(TypeError, match=match):
        Ellipse(
            x=0,
            y=0,
            radiusx=10,
            radiusy=10,
            anticlockwise=anti,
            counterclockwise=counter,
        )
