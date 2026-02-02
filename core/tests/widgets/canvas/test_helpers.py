from math import pi

from pytest import approx

from toga.widgets.canvas import arc_to_bezier, arc_to_quad_points, sweepangle


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


def assert_arc_to_quad_points(args, expected):
    actual = arc_to_quad_points(*args)
    for a, e in zip(actual, expected, strict=True):
        assert a[0] == approx(e[0], abs=0.000001)
        assert a[1] == approx(e[1], abs=0.000001)


def test_arc_to_quad_points():
    assert_arc_to_quad_points(
        [(10, 10), (20, 10), (20, 20), 10],
        [
            (10, 10),
            (14.1421356, 10),
            (17.07106781, 12.92893218),
            (20, 15.85786437),
            (20, 20),
        ],
    )
    assert_arc_to_quad_points(
        [(0, 10), (20, 10), (20, 30), 10],
        [
            (10, 10),
            (14.1421356, 10),
            (17.07106781, 12.92893218),
            (20, 15.85786437),
            (20, 20),
        ],
    )
    assert_arc_to_quad_points(
        [(15, 10), (20, 10), (20, 15), 10],
        [
            (10, 10),
            (14.1421356, 10),
            (17.07106781, 12.92893218),
            (20, 15.85786437),
            (20, 20),
        ],
    )

    # straight
    assert_arc_to_quad_points([(10, 10), (20, 10), (30, 10), 10], [(20, 10)])
    assert_arc_to_quad_points([(0, 10), (20, 10), (40, 10), 10], [(20, 10)])
    assert_arc_to_quad_points([(15, 10), (20, 10), (25, 10), 10], [(20, 10)])

    # 180 degrees
    assert_arc_to_quad_points([(10, 10), (20, 10), (10, 10), 10], [(20, 10)])
    assert_arc_to_quad_points([(15, 10), (20, 10), (15, 10), 10], [(20, 10)])
    assert_arc_to_quad_points([(5, 10), (20, 10), (5, 10), 10], [(20, 10)])

    # radius 0
    assert_arc_to_quad_points([(10, 10), (20, 10), (20, 20), 0], [(20, 10)])

    # identical points
    assert_arc_to_quad_points([(20, 10), (20, 10), (20, 10), 10], [(20, 10)])
