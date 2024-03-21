from travertino.size import at_least

from toga.style.pack import COLUMN, ROW, Pack

from ..utils import ExampleNode, ExampleViewport, assert_layout


def test_row_expanding_intrinsic():
    """Children in a row layout with fixed size don't expand, even if their hints allow
    it."""
    root = ExampleNode(
        "app",
        style=Pack(direction=ROW),
        children=[
            ExampleNode(
                "first",
                style=Pack(width=100, height=100),
                size=(at_least(0), at_least(0)),
            ),
            ExampleNode(
                "second",
                style=Pack(direction=ROW, width=100, height=100),
                size=(at_least(50), at_least(50)),
                children=[
                    ExampleNode(
                        "child",
                        style=Pack(width=50, height=50),
                        size=(at_least(0), at_least(0)),
                    ),
                ],
            ),
            ExampleNode(
                "third",
                style=Pack(width=0, height=0),  # Explicitly 0 sized
                size=(at_least(0), at_least(0)),
            ),
        ],
    )

    root.style.layout(root, ExampleViewport(640, 480))
    assert_layout(
        root,
        (200, 100),
        (640, 480),
        {
            "origin": (0, 0),
            "content": (640, 480),
            "children": [
                {
                    "origin": (0, 0),
                    "content": (100, 100),
                },
                {
                    "origin": (100, 0),
                    "content": (100, 100),
                    "children": [
                        {"origin": (100, 0), "content": (50, 50)},
                    ],
                },
                {
                    "origin": (200, 0),
                    "content": (0, 0),
                },
            ],
        },
    )


def test_row_fixed_intrinsic():
    """Children in a row layout without an explicit size, but a fixed intrinsic width,
    don't expand."""
    root = ExampleNode(
        "app",
        style=Pack(direction=ROW),
        children=[
            ExampleNode(
                "first",
                style=Pack(),
                size=(100, 100),
            ),
            ExampleNode(
                "second",
                style=Pack(direction=ROW),
                children=[
                    ExampleNode(
                        "child",
                        style=Pack(),
                        size=(50, 50),
                    ),
                ],
            ),
            ExampleNode(  # Explicitly 0 sized
                "third",
                style=Pack(),
                size=(0, 0),
            ),
        ],
    )

    root.style.layout(root, ExampleViewport(640, 480))
    assert_layout(
        root,
        (150, 100),
        (640, 480),
        {
            "origin": (0, 0),
            "content": (640, 480),
            "children": [
                {
                    "origin": (0, 0),
                    "content": (100, 100),
                },
                {
                    "origin": (100, 0),
                    "content": (50, 480),
                    "children": [
                        {"origin": (100, 0), "content": (50, 50)},
                    ],
                },
                {
                    "origin": (150, 0),
                    "content": (0, 0),
                },
            ],
        },
    )


def test_column_expanding_intrinsic():
    """Children in a column layout with fixed size don't expand, even if their hints
    allow it."""
    root = ExampleNode(
        "app",
        style=Pack(direction=COLUMN),
        children=[
            ExampleNode(
                "first",
                style=Pack(width=100, height=100),
                size=(at_least(0), at_least(0)),
            ),
            ExampleNode(
                "second",
                style=Pack(direction=COLUMN, width=100, height=100),
                size=(at_least(50), at_least(50)),
                children=[
                    ExampleNode(
                        "child",
                        style=Pack(width=50, height=50),
                        size=(at_least(0), at_least(0)),
                    ),
                ],
            ),
            ExampleNode(  # Explicitly 0 sized
                "third",
                style=Pack(width=0, height=0),
                size=(at_least(0), at_least(0)),
            ),
        ],
    )

    # Normal size
    root.style.layout(root, ExampleViewport(640, 480))
    assert_layout(
        root,
        (100, 200),
        (640, 480),
        {
            "origin": (0, 0),
            "content": (640, 480),
            "children": [
                {"origin": (0, 0), "content": (100, 100)},
                {
                    "origin": (0, 100),
                    "content": (100, 100),
                    "children": [
                        {"origin": (0, 100), "content": (50, 50)},
                    ],
                },
                {
                    "origin": (0, 200),
                    "content": (0, 0),
                },
            ],
        },
    )


def test_column_fixed_intrinsic():
    """Children in a column layout without an explicit size, but a fixed intrinsic
    width, don't expand."""
    root = ExampleNode(
        "app",
        style=Pack(direction=COLUMN),
        children=[
            ExampleNode(
                "first",
                style=Pack(),
                size=(100, 100),
            ),
            ExampleNode(
                "second",
                style=Pack(direction=COLUMN),
                children=[
                    ExampleNode(
                        "child",
                        style=Pack(),
                        size=(50, 50),
                    ),
                ],
            ),
            ExampleNode(  # Explicitly 0 sized
                "third",
                style=Pack(),
                size=(0, 0),
            ),
        ],
    )

    root.style.layout(root, ExampleViewport(640, 480))
    assert_layout(
        root,
        (100, 150),
        (640, 480),
        {
            "origin": (0, 0),
            "content": (640, 480),
            "children": [
                {
                    "origin": (0, 0),
                    "content": (100, 100),
                },
                {
                    "origin": (0, 100),
                    "content": (640, 50),
                    "children": [
                        {"origin": (0, 100), "content": (50, 50)},
                    ],
                },
                {
                    "origin": (0, 150),
                    "content": (0, 0),
                },
            ],
        },
    )
