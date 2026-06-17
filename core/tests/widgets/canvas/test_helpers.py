from math import pi

from pytest import approx, mark, raises

from toga.widgets.canvas.geometry import (
    arc_to_bezier,
    get_round_rect_radii,
    round_rect,
    sweepangle,
)
from toga_dummy.widgets.canvas import Canvas, Context


def test_sweepangle():
    # Zero start angles
    for value in [0, 1, pi, 2 * pi]:
        assert sweepangle(0, value, False) == approx(value)

    for value in [2.1 * pi, 3 * pi, 4 * pi, 5 * pi]:
        assert sweepangle(0, value, False) == approx(2 * pi)

    # Non-zero start angles
    assert sweepangle(pi, 2 * pi, False) == approx(pi)
    assert sweepangle(pi, 2.5 * pi, False) == approx(1.5 * pi)
    assert sweepangle(pi, 3 * pi, False) == approx(2 * pi)
    assert sweepangle(pi, 3.1 * pi, False) == approx(2 * pi)

    # Zero crossings
    assert sweepangle(0, 2 * pi, False) == approx(2 * pi)
    assert sweepangle(0, -2 * pi, False) == approx(0)
    assert sweepangle(0, 1.9 * pi, False) == approx(1.9 * pi)
    assert sweepangle(0, 2.1 * pi, False) == approx(2 * pi)
    assert sweepangle(0, -1.9 * pi, False) == approx(0.1 * pi)
    assert sweepangle(0, -2.1 * pi, False) == approx(1.9 * pi)
    assert sweepangle(pi, 0, False) == approx(pi)
    assert sweepangle(pi, 2 * pi, False) == approx(pi)
    assert sweepangle(pi, 0.1 * pi, False) == approx(1.1 * pi)
    assert sweepangle(pi, 2.1 * pi, False) == approx(1.1 * pi)

    # Zero crossings, counterclockwise
    assert sweepangle(0, 2 * pi, True) == approx(0)
    assert sweepangle(0, -2 * pi, True) == approx(-2 * pi)
    assert sweepangle(0, 1.9 * pi, True) == approx(-0.1 * pi)
    assert sweepangle(0, 2.1 * pi, True) == approx(-1.9 * pi)
    assert sweepangle(0, -1.9 * pi, True) == approx(-1.9 * pi)
    assert sweepangle(0, -2.1 * pi, True) == approx(-2 * pi)
    assert sweepangle(pi, 0, True) == approx(-pi)
    assert sweepangle(pi, 2 * pi, True) == approx(-pi)
    assert sweepangle(pi, 0.1 * pi, True) == approx(-0.9 * pi)
    assert sweepangle(pi, 2.1 * pi, True) == approx(-0.9 * pi)


def assert_arc_to_bezier(sweepangle, expected):
    actual = arc_to_bezier(sweepangle)
    for a, e in zip(actual, expected, strict=False):
        assert a == approx(e, abs=0.000001)


def test_arc_to_bezier():
    assert_arc_to_bezier(
        0,
        [
            (1.0, 0.0),
            (1.0, 0.0),
            (1.0, 0.0),
            (1.0, 0.0),
        ],
    )

    assert_arc_to_bezier(
        0.25 * pi,
        [
            (1.0, 0.0),
            (1.0, 0.2652164),
            (0.8946431, 0.5195704),
            (0.7071067, 0.7071067),
        ],
    )
    assert_arc_to_bezier(
        -0.25 * pi,
        [
            (1.0, 0.0),
            (1.0, -0.2652164),
            (0.8946431, -0.5195704),
            (0.7071067, -0.7071067),
        ],
    )

    assert_arc_to_bezier(
        0.5 * pi,
        [
            (1.0, 0.0),
            (1.0, 0.5522847),
            (0.5522847, 1.0),
            (0.0, 1.0),
        ],
    )
    assert_arc_to_bezier(
        -0.5 * pi,
        [
            (1.0, 0.0),
            (1.0, -0.5522847),
            (0.5522847, -1.0),
            (0.0, -1.0),
        ],
    )

    assert_arc_to_bezier(
        0.75 * pi,
        [
            (1.0, 0.0),
            (1.0, 0.5522847),
            (0.5522847, 1.0),
            (0.0, 1.0),
            (-0.2652164, 1.0),
            (-0.5195704, 0.8946431),
            (-0.7071067, 0.7071067),
        ],
    )
    assert_arc_to_bezier(
        -0.75 * pi,
        [
            (1.0, 0.0),
            (1.0, -0.5522847),
            (0.5522847, -1.0),
            (0.0, -1.0),
            (-0.2652164, -1.0),
            (-0.5195704, -0.8946431),
            (-0.7071067, -0.7071067),
        ],
    )

    assert_arc_to_bezier(
        1 * pi,
        [
            (1.0, 0.0),
            (1.0, 0.5522847),
            (0.5522847, 1.0),
            (0.0, 1.0),
            (-0.5522847, 1.0),
            (-1.0, 0.5522847),
            (-1.0, 0.0),
        ],
    )
    assert_arc_to_bezier(
        -1 * pi,
        [
            (1.0, 0.0),
            (1.0, -0.5522847),
            (0.5522847, -1.0),
            (0.0, -1.0),
            (-0.5522847, -1.0),
            (-1.0, -0.5522847),
            (-1.0, 0.0),
        ],
    )

    assert_arc_to_bezier(
        1.5 * pi,
        [
            (1.0, 0.0),
            (1.0, 0.5522847),
            (0.5522847, 1.0),
            (0.0, 1.0),
            (-0.5522847, 1.0),
            (-1.0, 0.5522847),
            (-1.0, 0.0),
            (-1.0, -0.5522847),
            (-0.5522847, -1.0),
            (0.0, -1.0),
        ],
    )
    assert_arc_to_bezier(
        -1.5 * pi,
        [
            (1.0, 0.0),
            (1.0, -0.5522847),
            (0.5522847, -1.0),
            (0.0, -1.0),
            (-0.5522847, -1.0),
            (-1.0, -0.5522847),
            (-1.0, 0.0),
            (-1.0, 0.5522847),
            (-0.5522847, 1.0),
            (0.0, 1.0),
        ],
    )

    assert_arc_to_bezier(
        2 * pi,
        [
            (1.0, 0.0),
            (1.0, 0.5522847),
            (0.5522847, 1.0),
            (0.0, 1.0),
            (-0.5522847, 1.0),
            (-1.0, 0.5522847),
            (-1.0, 0.0),
            (-1.0, -0.5522847),
            (-0.5522847, -1.0),
            (0.0, -1.0),
            (0.5522847, -1.0),
            (1.0, -0.5522847),
            (1.0, 0.0),
        ],
    )
    assert_arc_to_bezier(
        -2 * pi,
        [
            (1.0, 0.0),
            (1.0, -0.5522847),
            (0.5522847, -1.0),
            (0.0, -1.0),
            (-0.5522847, -1.0),
            (-1.0, -0.5522847),
            (-1.0, 0.0),
            (-1.0, 0.5522847),
            (-0.5522847, 1.0),
            (0.0, 1.0),
            (0.5522847, 1.0),
            (1.0, 0.5522847),
            (1.0, 0.0),
        ],
    )


def test_round_rect():
    canvas = Canvas(None)
    canvas.draw_instructions = []
    context = Context(canvas)

    round_rect(context, 10, 20, 30, 40, 5)
    assert canvas.draw_instructions == [
        ("move to", {"x": 15, "y": 20}),
        ("line to", {"x": 35, "y": 20}),
        (
            "ellipse",
            {
                "x": 35,
                "y": 25,
                "radiusx": 5,
                "radiusy": 5,
                "rotation": 0,
                "startangle": -pi / 2,
                "endangle": 0,
                "counterclockwise": False,
            },
        ),
        ("line to", {"x": 40, "y": 55}),
        (
            "ellipse",
            {
                "x": 35,
                "y": 55,
                "radiusx": 5,
                "radiusy": 5,
                "rotation": 0,
                "startangle": 0,
                "endangle": pi / 2,
                "counterclockwise": False,
            },
        ),
        ("line to", {"x": 15, "y": 60}),
        (
            "ellipse",
            {
                "x": 15,
                "y": 55,
                "radiusx": 5,
                "radiusy": 5,
                "rotation": 0,
                "startangle": pi / 2,
                "endangle": pi,
                "counterclockwise": False,
            },
        ),
        ("line to", {"x": 10, "y": 25}),
        (
            "ellipse",
            {
                "x": 15,
                "y": 25,
                "radiusx": 5,
                "radiusy": 5,
                "rotation": 0,
                "startangle": pi,
                "endangle": 3 * pi / 2,
                "counterclockwise": False,
            },
        ),
        ("move to", {"x": 10, "y": 20}),
    ]


class Radius:
    x: float
    y: float

    def __init__(self, x, y):
        self.x = x
        self.y = y


@mark.parametrize(
    "w, h, radii, expected",
    # argument handling
    [
        (20, 30, 5, [(5, 5), (5, 5), (5, 5), (5, 5)]),
        (20, 30, 5.5, [(5.5, 5.5), (5.5, 5.5), (5.5, 5.5), (5.5, 5.5)]),
        (20, 30, [5], [(5, 5), (5, 5), (5, 5), (5, 5)]),
        (20, 30, [5, 6], [(5, 5), (6, 6), (6, 6), (5, 5)]),
        (20, 30, [5, 6, 7], [(5, 5), (6, 6), (6, 6), (7, 7)]),
        (20, 30, [5, 6, 7, 8], [(5, 5), (6, 6), (7, 7), (8, 8)]),
        (20, 30, Radius(5, 6), [(5, 6), (5, 6), (5, 6), (5, 6)]),
        (20, 30, [Radius(5, 6)], [(5, 6), (5, 6), (5, 6), (5, 6)]),
        (20, 30, [Radius(5, 6), 7], [(5, 6), (7, 7), (7, 7), (5, 6)]),
        # scaling needed
        (10, 20, 10, [(5, 5), (5, 5), (5, 5), (5, 5)]),
        (20, 20, Radius(5, 20), [(2.5, 10), (2.5, 10), (2.5, 10), (2.5, 10)]),
        # negative width and/or height
        (-20, 30, 5, [(-5, 5), (-5, 5), (-5, 5), (-5, 5)]),
        (20, -30, 5, [(5, -5), (5, -5), (5, -5), (5, -5)]),
        # degenerate cases
        (0, 20, 5, [(0, 0), (0, 0), (0, 0), (0, 0)]),
        (20, 0, 5, [(0, 0), (0, 0), (0, 0), (0, 0)]),
    ],
)
def test_get_round_rect_radii(w, h, radii, expected):
    actual = get_round_rect_radii(w, h, radii)
    assert actual == expected


def test_get_round_rect_radii_errors():
    # radii length
    with raises(
        ValueError,
        match=r"Invalid radii: \[\], expected length between 1 and 4 items",
    ):
        get_round_rect_radii(20, 30, [])

    with raises(
        ValueError,
        match=(
            r"Invalid radii: \[1, 2, 3, 4, 5\], expected length between 1 and 4 items"
        ),
    ):
        get_round_rect_radii(20, 30, [1, 2, 3, 4, 5])
