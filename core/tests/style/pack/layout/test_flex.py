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

    # Minimum size
    root.style.layout(root, ExampleViewport(0, 0, dpi=96))
    assert_layout(
        root,
        (50, 50),
        {
            "origin": (0, 0),
            "content": (50, 50),
            "children": [
                {
                    "origin": (0, 0),
                    "content": (0, 0),
                },
                {
                    "origin": (0, 0),
                    "content": (50, 50),
                    "children": [
                        {"origin": (0, 0), "content": (50, 50)},
                    ],
                },
            ],
        },
    )

    # Normal size
    root.style.layout(root, ExampleViewport(640, 480, dpi=96))
    assert_layout(
        root,
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

    # HiDPI Normal size
    root.style.layout(root, ExampleViewport(640, 480, dpi=144))
    assert_layout(
        root,
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
                        {"origin": (320, 0), "content": (75, 75)},
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

    # Minimum size
    root.style.layout(root, ExampleViewport(0, 0, dpi=96))
    assert_layout(
        root,
        (300, 100),
        {
            "origin": (0, 0),
            "content": (300, 100),
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

    # # Normal size
    root.style.layout(root, ExampleViewport(640, 480, dpi=96))
    assert_layout(
        root,
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

    # # HiDPI Normal size
    root.style.layout(root, ExampleViewport(640, 480, dpi=144))
    assert_layout(
        root,
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
                        {"origin": (100, 0), "content": (30, 30)},
                        {"origin": (130, 0), "content": (20, 20)},
                        {"origin": (150, 0), "content": (20, 100)},
                        {"origin": (170, 0), "content": (55, 100)},
                        {"origin": (225, 0), "content": (20, 20)},
                        {"origin": (245, 0), "content": (55, 100)},
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

    # Minimum size
    root.style.layout(root, ExampleViewport(0, 0, dpi=96))
    assert_layout(
        root,
        (200, 100),
        {
            "origin": (0, 0),
            "content": (200, 100),
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

    # # Normal size
    root.style.layout(root, ExampleViewport(640, 480, dpi=96))
    assert_layout(
        root,
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

    # # HiDPI Normal size
    root.style.layout(root, ExampleViewport(640, 480, dpi=144))
    assert_layout(
        root,
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
                    "content": (110, 100),
                    "children": [
                        {"origin": (100, 0), "content": (30, 30)},
                        {"origin": (130, 0), "content": (20, 20)},
                        {"origin": (150, 0), "content": (20, 100)},
                        {"origin": (170, 0), "content": (0, 100)},
                        {"origin": (170, 0), "content": (20, 20)},
                        {"origin": (190, 0), "content": (20, 100)},
                    ],
                },
            ],
        },
    )


def test_column_flex_no_hints():
    """Children in a column layout with flexible containers, but no flex hints,
    doesn't collapse column width."""
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

    # Minimum size
    root.style.layout(root, ExampleViewport(0, 0, dpi=96))
    assert_layout(
        root,
        (50, 50),
        {
            "origin": (0, 0),
            "content": (50, 50),
            "children": [
                {
                    "origin": (0, 0),
                    "content": (0, 0),
                },
                {
                    "origin": (0, 0),
                    "content": (50, 50),
                    "children": [
                        {"origin": (0, 0), "content": (50, 50)},
                    ],
                },
            ],
        },
    )

    # # Normal size
    root.style.layout(root, ExampleViewport(640, 480, dpi=96))
    assert_layout(
        root,
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

    # # HiDPI Normal size
    root.style.layout(root, ExampleViewport(640, 480, dpi=144))
    assert_layout(
        root,
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
                        {"origin": (0, 240), "content": (75, 75)},
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

    # Minimum size
    root.style.layout(root, ExampleViewport(0, 0, dpi=96))
    assert_layout(
        root,
        (100, 300),
        {
            "origin": (0, 0),
            "content": (100, 300),
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

    # Normal size
    root.style.layout(root, ExampleViewport(640, 480, dpi=96))
    assert_layout(
        root,
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

    # HiDPI Normal size
    root.style.layout(root, ExampleViewport(640, 480, dpi=144))
    assert_layout(
        root,
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
                        {"origin": (0, 100), "content": (30, 30)},
                        {"origin": (0, 130), "content": (20, 20)},
                        {"origin": (0, 150), "content": (100, 20)},
                        {"origin": (0, 170), "content": (100, 55)},
                        {"origin": (0, 225), "content": (20, 20)},
                        {"origin": (0, 245), "content": (100, 55)},
                    ],
                },
            ],
        },
    )


def test_column_flex_insufficient_space():
    """Children in a column layout with flexible containers, but insufficient space to
    accommodate them, and an explicit intrinsic width, doesn't collapse column width.
    """

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

    # Minimum size
    root.style.layout(root, ExampleViewport(0, 0, dpi=96))
    assert_layout(
        root,
        (100, 200),
        {
            "origin": (0, 0),
            "content": (100, 200),
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

    # Normal size
    root.style.layout(root, ExampleViewport(640, 480, dpi=96))
    assert_layout(
        root,
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

    # HiDPI Normal size
    root.style.layout(root, ExampleViewport(640, 480, dpi=144))
    assert_layout(
        root,
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
                    "content": (100, 110),
                    "children": [
                        {"origin": (0, 100), "content": (30, 30)},
                        {"origin": (0, 130), "content": (20, 20)},
                        {"origin": (0, 150), "content": (100, 20)},
                        {"origin": (0, 170), "content": (100, 0)},
                        {"origin": (0, 170), "content": (20, 20)},
                        {"origin": (0, 190), "content": (100, 20)},
                    ],
                },
            ],
        },
    )
