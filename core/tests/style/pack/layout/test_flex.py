from travertino.size import at_least

from toga.style.pack import COLUMN, ROW, Pack

from ..utils import ExampleNode, ExampleViewport, assert_layout


def test_row_flex_no_hints():
    """Child in a row layout with flexible containers, but no flex hints, doesn't
    collapse row height."""
    root = ExampleNode(
        "app",
        style=Pack(direction=ROW),
        children=[
            ExampleNode(
                "first",
                style=Pack(flex=1),
            ),
            ExampleNode(
                "second",
                style=Pack(direction=ROW, flex=1),
                children=[
                    ExampleNode(
                        "child",
                        style=Pack(width=50, height=50),
                    ),
                ],
            ),
        ],
    )

    root.style.layout(root, ExampleViewport(640, 480))
    assert_layout(
        root,
        (50, 50),
        (640, 480),
        {
            "origin": (0, 0),
            "content": (640, 480),
            "children": [
                {
                    "origin": (0, 0),
                    "content": (320, 480),
                },
                {
                    "origin": (320, 0),
                    "content": (320, 480),
                    "children": [
                        {"origin": (320, 0), "content": (50, 50)},
                    ],
                },
            ],
        },
    )


def test_row_flex():
    """Children in a row layout with flexible containers, and an explicit intrinsic
    width doesn't collapse row height."""
    root = ExampleNode(
        "app",
        style=Pack(direction=ROW),
        children=[
            ExampleNode(
                "first",
                style=Pack(flex=1),
                size=(100, 100),
            ),
            ExampleNode(
                "second",
                style=Pack(direction=ROW, flex=1),
                size=(200, 100),
                children=[
                    ExampleNode(  # Explicit size
                        "child 1",
                        style=Pack(width=20, height=20),
                    ),
                    ExampleNode(  # No size, Explicit intrinsic
                        "child 2",
                        style=Pack(),
                        size=(20, 20),
                    ),
                    ExampleNode(  # No size, explicit expanding intrinsic
                        "child 3",
                        style=Pack(),
                        size=(at_least(20), at_least(20)),
                    ),
                    ExampleNode(  # Flexible size, no intrinsic
                        "child 4",
                        style=Pack(flex=1),
                    ),
                    ExampleNode(  # Flexible size with explicit intrinsic
                        "child 5",
                        style=Pack(flex=1),
                        size=(20, 20),
                    ),
                    ExampleNode(  # Flexible size with explicit expanding intrinsic
                        "child 6",
                        style=Pack(flex=1),
                        size=(at_least(20), at_least(20)),
                    ),
                ],
            ),
        ],
    )

    root.style.layout(root, ExampleViewport(640, 480))
    assert_layout(
        root,
        (300, 100),
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
                    "content": (200, 100),
                    "children": [
                        {"origin": (100, 0), "content": (20, 20)},
                        {"origin": (120, 0), "content": (20, 20)},
                        {"origin": (140, 0), "content": (20, 100)},
                        {"origin": (160, 0), "content": (60, 100)},
                        {"origin": (220, 0), "content": (20, 20)},
                        {"origin": (240, 0), "content": (60, 100)},
                    ],
                },
            ],
        },
    )


def test_row_flex_insufficient_space():
    """Children in a row layout with flexible containers, but insufficient_space, and an
    explicit intrinsic width doesn't collapse row height."""
    root = ExampleNode(
        "app",
        style=Pack(direction=ROW),
        children=[
            ExampleNode(
                "first",
                style=Pack(flex=1),
                size=(100, 100),
            ),
            ExampleNode(
                "second",
                style=Pack(direction=ROW, flex=1),
                size=(100, 100),
                children=[
                    ExampleNode(  # Explicit size
                        "child 1",
                        style=Pack(width=20, height=20),
                    ),
                    ExampleNode(  # No size, Explicit intrinsic
                        "child 2",
                        style=Pack(),
                        size=(20, 20),
                    ),
                    ExampleNode(  # No size, explicit expanding intrinsic
                        "child 3",
                        style=Pack(),
                        size=(at_least(20), at_least(20)),
                    ),
                    ExampleNode(  # Flexible size, no intrinsic
                        "child 4",
                        style=Pack(flex=1),
                    ),
                    ExampleNode(  # Flexible size with explicit intrinsic
                        "child 5",
                        style=Pack(flex=1),
                        size=(20, 20),
                    ),
                    ExampleNode(  # Flexible size with explicit expanding intrinsic
                        "child 6",
                        style=Pack(flex=1),
                        size=(at_least(20), at_least(20)),
                    ),
                ],
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
                        {"origin": (100, 0), "content": (20, 20)},
                        {"origin": (120, 0), "content": (20, 20)},
                        {"origin": (140, 0), "content": (20, 100)},
                        {"origin": (160, 0), "content": (0, 100)},
                        {"origin": (160, 0), "content": (20, 20)},
                        {"origin": (180, 0), "content": (20, 100)},
                    ],
                },
            ],
        },
    )


def test_row_flex_insufficient_space_no_flex():
    """Children in a row layout with flexible containers, but insufficient_space for any
    of the flexible content, and an explicit intrinsic width, doesn't collapse row
    height."""
    root = ExampleNode(
        "app",
        style=Pack(direction=ROW),
        children=[
            ExampleNode(
                "first",
                style=Pack(flex=1),
                size=(100, 100),
            ),
            ExampleNode(
                "second",
                style=Pack(direction=ROW, flex=1),
                size=(100, 100),
                children=[
                    # All children are expanding flexible, but the intrinsic minimum
                    # size is greater than what is available.
                    ExampleNode(
                        "child 1",
                        style=Pack(flex=1),
                        size=(at_least(60), 20),
                    ),
                    ExampleNode(
                        "child 2",
                        style=Pack(flex=1),
                        size=(at_least(60), 30),
                    ),
                ],
            ),
        ],
    )

    root.style.layout(root, ExampleViewport(640, 480))
    assert_layout(
        root,
        (220, 100),
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
                    "content": (120, 100),
                    "children": [
                        {"origin": (100, 0), "content": (60, 20)},
                        {"origin": (160, 0), "content": (60, 30)},
                    ],
                },
            ],
        },
    )


def test_row_flex_grandchild_min_size():
    """The minimum intrinsic sizes of grandchild of flex row containers are honored."""
    root = ExampleNode(
        "app",
        size=(at_least(0), at_least(0)),
        style=Pack(direction=ROW),
        children=[
            ExampleNode(
                "inner",
                size=(at_least(0), at_least(0)),
                style=Pack(direction=COLUMN, flex=1),
                children=[
                    ExampleNode(
                        "textbox",
                        size=(at_least(100), at_least(100)),
                        style=Pack(flex=1),
                    )
                ],
            ),
            ExampleNode(
                "Button",
                size=(20, at_least(100)),
                style=Pack(),
            ),
        ],
    )

    root.style.layout(root, ExampleViewport(640, 480))
    assert_layout(
        root,
        (120, 100),
        (640, 480),
        {
            "origin": (0, 0),
            "content": (640, 480),
            "children": [
                {
                    "origin": (0, 0),
                    "content": (620, 480),
                    "children": [
                        {"origin": (0, 0), "content": (620, 480)},
                    ],
                },
                {
                    "origin": (620, 0),
                    "content": (20, 480),
                },
            ],
        },
    )


def test_column_flex_no_hints():
    """Children in a column layout with flexible containers, but no flex hints, doesn't
    collapse column width."""
    root = ExampleNode(
        "app",
        style=Pack(direction=COLUMN),
        children=[
            ExampleNode(
                "first",
                style=Pack(flex=1),
            ),
            ExampleNode(
                "second",
                style=Pack(direction=COLUMN, flex=1),
                children=[
                    ExampleNode(
                        "child",
                        style=Pack(width=50, height=50),
                    ),
                ],
            ),
        ],
    )

    root.style.layout(root, ExampleViewport(640, 480))
    assert_layout(
        root,
        (50, 50),
        (640, 480),
        {
            "origin": (0, 0),
            "content": (640, 480),
            "children": [
                {
                    "origin": (0, 0),
                    "content": (640, 240),
                },
                {
                    "origin": (0, 240),
                    "content": (640, 240),
                    "children": [
                        {"origin": (0, 240), "content": (50, 50)},
                    ],
                },
            ],
        },
    )


def test_column_flex():
    """Children in a column layout with flexible containers, and an explicit intrinsic
    width, doesn't collapse column width."""
    root = ExampleNode(
        "app",
        style=Pack(direction=COLUMN),
        children=[
            ExampleNode(
                "first",
                style=Pack(flex=1),
                size=(100, 100),
            ),
            ExampleNode(
                "second",
                style=Pack(direction=COLUMN, flex=1),
                size=(100, 200),
                children=[
                    ExampleNode(  # Explicit size
                        "child 1",
                        style=Pack(width=20, height=20),
                    ),
                    ExampleNode(  # No size, Explicit intrinsic
                        "child 2",
                        style=Pack(),
                        size=(20, 20),
                    ),
                    ExampleNode(  # No size, explicit expanding intrinsic
                        "child 3",
                        style=Pack(),
                        size=(at_least(20), at_least(20)),
                    ),
                    ExampleNode(  # Flexible size, no intrinsic
                        "child 4",
                        style=Pack(flex=1),
                    ),
                    ExampleNode(  # Flexible size with explicit intrinsic
                        "child 5",
                        style=Pack(flex=1),
                        size=(20, 20),
                    ),
                    ExampleNode(  # Flexible size with explicit expanding intrinsic
                        "child 6",
                        style=Pack(flex=1),
                        size=(at_least(20), at_least(20)),
                    ),
                ],
            ),
        ],
    )

    root.style.layout(root, ExampleViewport(640, 480))
    assert_layout(
        root,
        (100, 300),
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
                    "content": (100, 200),
                    "children": [
                        {"origin": (0, 100), "content": (20, 20)},
                        {"origin": (0, 120), "content": (20, 20)},
                        {"origin": (0, 140), "content": (100, 20)},
                        {"origin": (0, 160), "content": (100, 60)},
                        {"origin": (0, 220), "content": (20, 20)},
                        {"origin": (0, 240), "content": (100, 60)},
                    ],
                },
            ],
        },
    )


def test_column_flex_insufficient_space():
    """Children in a column layout with flexible containers, but insufficient space to
    accommodate them, and an explicit intrinsic width, doesn't collapse column width."""

    root = ExampleNode(
        "app",
        style=Pack(direction=COLUMN),
        children=[
            ExampleNode(
                "first",
                style=Pack(flex=1),
                size=(100, 100),
            ),
            ExampleNode(
                "second",
                style=Pack(direction=COLUMN, flex=1),
                size=(100, 100),
                children=[
                    ExampleNode(  # Explicit size
                        "child 1",
                        style=Pack(width=20, height=20),
                    ),
                    ExampleNode(  # No size, Explicit intrinsic
                        "child 2",
                        style=Pack(),
                        size=(20, 20),
                    ),
                    ExampleNode(  # No size, explicit expanding intrinsic
                        "child 3",
                        style=Pack(),
                        size=(at_least(20), at_least(20)),
                    ),
                    ExampleNode(  # Flexible size, no intrinsic
                        "child 4",
                        style=Pack(flex=1),
                    ),
                    ExampleNode(  # Flexible size with explicit intrinsic
                        "child 5",
                        style=Pack(flex=1),
                        size=(20, 20),
                    ),
                    ExampleNode(  # Flexible size with explicit expanding intrinsic
                        "child 6",
                        style=Pack(flex=1),
                        size=(at_least(20), at_least(20)),
                    ),
                ],
            ),
        ],
    )

    root.style.layout(root, ExampleViewport(640, 480))
    assert_layout(
        root,
        (100, 200),
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
                    "content": (100, 100),
                    "children": [
                        {"origin": (0, 100), "content": (20, 20)},
                        {"origin": (0, 120), "content": (20, 20)},
                        {"origin": (0, 140), "content": (100, 20)},
                        {"origin": (0, 160), "content": (100, 0)},
                        {"origin": (0, 160), "content": (20, 20)},
                        {"origin": (0, 180), "content": (100, 20)},
                    ],
                },
            ],
        },
    )


def test_column_flex_insufficient_space_no_flex():
    """Children in a column layout with flexible containers, but insufficient space for
    any of the flexible content, and an explicit intrinsic width, doesn't collapse
    column width."""

    root = ExampleNode(
        "app",
        style=Pack(direction=COLUMN),
        children=[
            ExampleNode(
                "first",
                style=Pack(flex=1),
                size=(100, 100),
            ),
            ExampleNode(
                "second",
                style=Pack(direction=COLUMN, flex=1),
                size=(100, 100),
                children=[
                    # All children are expanding flexible, but the intrinsic minimum
                    # size is greater than what is available.
                    ExampleNode(
                        "child 1",
                        style=Pack(flex=1),
                        size=(20, at_least(60)),
                    ),
                    ExampleNode(
                        "child 2",
                        style=Pack(flex=1),
                        size=(30, at_least(60)),
                    ),
                ],
            ),
        ],
    )

    root.style.layout(root, ExampleViewport(640, 480))
    assert_layout(
        root,
        (100, 220),
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
                    "content": (100, 120),
                    "children": [
                        {"origin": (0, 100), "content": (20, 60)},
                        {"origin": (0, 160), "content": (30, 60)},
                    ],
                },
            ],
        },
    )


def test_column_flex_grandchild_min_size():
    """The minimum intrinsic sizes of grandchild of flex column containers are
    honored."""
    root = ExampleNode(
        "app",
        size=(at_least(0), at_least(0)),
        style=Pack(direction=COLUMN),
        children=[
            ExampleNode(
                "inner",
                size=(at_least(0), at_least(0)),
                style=Pack(direction=ROW, flex=1),
                children=[
                    ExampleNode(
                        "textbox",
                        size=(at_least(100), at_least(100)),
                        style=Pack(flex=1),
                    )
                ],
            ),
            ExampleNode(
                "Button",
                size=(at_least(100), 20),
                style=Pack(),
            ),
        ],
    )

    root.style.layout(root, ExampleViewport(640, 480))
    assert_layout(
        root,
        (100, 120),
        (640, 480),
        {
            "origin": (0, 0),
            "content": (640, 480),
            "children": [
                {
                    "origin": (0, 0),
                    "content": (640, 460),
                    "children": [
                        {"origin": (0, 0), "content": (640, 460)},
                    ],
                },
                {
                    "origin": (0, 460),
                    "content": (640, 20),
                },
            ],
        },
    )
