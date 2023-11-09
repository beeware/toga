from math import pi

from pytest import approx

from toga.widgets.canvas import arc_to_bezier, sweepangle


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

    # Zero crossings, anticlockwise
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
    for a, e in zip(actual, expected):
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
