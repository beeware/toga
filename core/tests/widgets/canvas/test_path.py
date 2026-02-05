import pytest

from toga.widgets.canvas import Path2D


@pytest.fixture()
def path():
    return Path2D()


def test_compile(path):
    path.move_to(100, 50)
    draw_op = path.line_to(200, 100)

    assert path.impl.draw_instructions == [
        ("move to", {"x": 100, "y": 50}),
        ("line to", {"x": 200, "y": 100}),
    ]

    # adding more to the path prompts recompilation
    path.line_to(100, 200)
    assert path.impl.draw_instructions == [
        ("move to", {"x": 100, "y": 50}),
        ("line to", {"x": 200, "y": 100}),
        ("line to", {"x": 100, "y": 200}),
    ]

    # but if you change an operation it doesn't change the path
    draw_op.x = 150
    assert path.impl.draw_instructions == [
        ("move to", {"x": 100, "y": 50}),
        ("line to", {"x": 200, "y": 100}),
        ("line to", {"x": 100, "y": 200}),
    ]

    # unless you explicitly recompile
    path.compile()
    assert path.impl.draw_instructions == [
        ("move to", {"x": 100, "y": 50}),
        ("line to", {"x": 150, "y": 100}),
        ("line to", {"x": 100, "y": 200}),
    ]


def test_create_path_from_path(path):
    path.move_to(100, 50)
    path.line_to(200, 100)

    new_path = Path2D(path)
    new_path.compile()

    assert new_path.impl.draw_instructions == [
        ("move to", {"x": 100, "y": 50}),
        ("line to", {"x": 200, "y": 100}),
    ]


def test_close_path(path):
    """A close path operation can be added."""
    draw_op = path.close_path()

    assert repr(draw_op) == "ClosePath()"

    # The first and last instructions save/restore the root state, and can be ignored.
    assert path.impl.draw_instructions == ["close path"]


@pytest.mark.parametrize(
    "transform, args_repr",
    [
        (None, "transform=None"),
        ((1, 2, 3, 4, 5, 6), "transform=(1, 2, 3, 4, 5, 6)"),
    ],
)
def test_add_path(path, transform, args_repr):
    """An add path operation can be added."""
    other_path = Path2D()
    other_path.move_to(100, 50)
    other_path.line_to(200, 100)

    draw_op = path.add_path(other_path, transform)

    assert repr(draw_op) == f"AddPath(path={other_path!r}, {args_repr})"

    assert path.impl.draw_instructions == [
        ("add path", {"path": other_path.impl, "transform": transform}),
    ]


def test_move_to(path):
    """A move to operation can be added."""
    draw_op = path.move_to(10, 20)

    assert repr(draw_op) == "MoveTo(x=10, y=20)"

    assert path.impl.draw_instructions == [
        ("move to", {"x": 10, "y": 20}),
    ]

    # All the attributes can be retrieved.
    assert draw_op.x == 10
    assert draw_op.y == 20


def test_line_to(path):
    """A line to operation can be added."""
    draw_op = path.line_to(10, 20)

    assert repr(draw_op) == "LineTo(x=10, y=20)"

    assert path.impl.draw_instructions == [
        ("line to", {"x": 10, "y": 20}),
    ]

    # All the attributes can be retrieved.
    assert draw_op.x == 10
    assert draw_op.y == 20


def test_bezier_curve_to(path):
    """A Bézier curve to operation can be added."""
    draw_op = path.bezier_curve_to(10, 20, 30, 40, 50, 60)

    assert (
        repr(draw_op) == "BezierCurveTo(cp1x=10, cp1y=20, cp2x=30, cp2y=40, x=50, y=60)"
    )

    assert path.impl.draw_instructions == [
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


def test_quadratic_curve_to(path):
    """A Quadratic curve to operation can be added."""
    draw_op = path.quadratic_curve_to(10, 20, 30, 40)

    assert repr(draw_op) == "QuadraticCurveTo(cpx=10, cpy=20, x=30, y=40)"

    assert path.impl.draw_instructions == [
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
def test_arc(path, kwargs, args_repr, draw_kwargs):
    """An arc operation can be added."""
    draw_op = path.arc(**kwargs)

    assert repr(draw_op) == f"Arc({args_repr})"

    assert path.impl.draw_instructions == [
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
def test_ellipse(path, kwargs, args_repr, draw_kwargs):
    """An ellipse operation can be added."""
    draw_op = path.ellipse(**kwargs)

    assert repr(draw_op) == f"Ellipse({args_repr})"

    assert path.impl.draw_instructions == [
        ("ellipse", draw_kwargs),
    ]

    # All the attributes can be retrieved.
    for attr, value in draw_kwargs.items():
        assert getattr(draw_op, attr) == value


def test_rect(path):
    """A rect operation can be added."""
    draw_op = path.rect(10, 20, 30, 40)

    assert repr(draw_op) == "Rect(x=10, y=20, width=30, height=40)"

    assert path.impl.draw_instructions == [
        ("rect", {"x": 10, "y": 20, "width": 30, "height": 40}),
    ]

    # All the attributes can be retrieved.
    assert draw_op.x == 10
    assert draw_op.y == 20
    assert draw_op.width == 30
    assert draw_op.height == 40


def test_round_rect(path):
    """A rect operation can be added."""
    draw_op = path.round_rect(10, 20, 30, 40, 5)

    assert repr(draw_op) == "RoundRect(x=10, y=20, width=30, height=40, radii=5)"

    assert path.impl.draw_instructions == [
        ("round rect", {"x": 10, "y": 20, "width": 30, "height": 40, "radii": 5}),
    ]

    # All the attributes can be retrieved.
    assert draw_op.x == 10
    assert draw_op.y == 20
    assert draw_op.width == 30
    assert draw_op.height == 40
    assert draw_op.radii == 5
